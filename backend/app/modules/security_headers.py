from typing import List, Dict, Optional
import httpx
from app.schemas.threat import SecurityHeaderFinding, IndicatorSeverity
from app.core.config import settings

class SecurityHeadersAuditor:
    @staticmethod
    async def audit_url_headers(target_url: str) -> List[SecurityHeaderFinding]:
        """
        Safely and passively retrieves and audits HTTP response headers for best-practice security controls.
        """
        findings: List[SecurityHeaderFinding] = []

        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS, verify=False) as client:
                response = await client.get(
                    target_url,
                    headers={"User-Agent": "AegisTrust-Security-Probe/1.0"},
                    follow_redirects=True
                )
                headers = {k.lower(): v for k, v in response.headers.items()}
        except Exception:
            # If network error or unreachable, return minimal baseline findings
            return [
                SecurityHeaderFinding(
                    header_name="HTTP Connectivity",
                    status="FAIL",
                    severity=IndicatorSeverity.MEDIUM,
                    value=None,
                    impact="Server did not respond to passive HTTP probes.",
                    remediation="Ensure the web service is online and accepting incoming connections on port 80/443."
                )
            ]

        # 1. Content-Security-Policy (CSP)
        csp = headers.get("content-security-policy")
        if not csp:
            findings.append(SecurityHeaderFinding(
                header_name="Content-Security-Policy",
                status="FAIL",
                severity=IndicatorSeverity.HIGH,
                value=None,
                impact="Leaves website exposed to Cross-Site Scripting (XSS) and arbitrary resource injection.",
                remediation="Configure a restrictive Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';"
            ))
        else:
            if "'unsafe-inline'" in csp or "'unsafe-eval'" in csp:
                findings.append(SecurityHeaderFinding(
                    header_name="Content-Security-Policy",
                    status="WARN",
                    severity=IndicatorSeverity.MEDIUM,
                    value=csp[:80] + "...",
                    impact="CSP contains 'unsafe-inline' or 'unsafe-eval', weakening script execution defenses.",
                    remediation="Remove 'unsafe-inline' and use cryptographic nonces or hashes for inline scripts."
                ))
            else:
                findings.append(SecurityHeaderFinding(
                    header_name="Content-Security-Policy",
                    status="PASS",
                    severity=IndicatorSeverity.INFO,
                    value=csp[:80] + "...",
                    impact="Strong CSP policy active against unauthorized script execution.",
                    remediation="Maintain existing CSP policy."
                ))

        # 2. Strict-Transport-Security (HSTS)
        hsts = headers.get("strict-transport-security")
        if not hsts:
            findings.append(SecurityHeaderFinding(
                header_name="Strict-Transport-Security",
                status="FAIL",
                severity=IndicatorSeverity.HIGH,
                value=None,
                impact="Allows SSL-stripping and man-in-the-middle downgrade attacks to unencrypted HTTP.",
                remediation="Enable HSTS: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
            ))
        else:
            if "max-age" in hsts:
                findings.append(SecurityHeaderFinding(
                    header_name="Strict-Transport-Security",
                    status="PASS",
                    severity=IndicatorSeverity.INFO,
                    value=hsts,
                    impact="Enforces persistent HTTPS encryption for all browser sessions.",
                    remediation="Maintain HSTS configuration."
                ))

        # 3. X-Frame-Options (Clickjacking)
        xfo = headers.get("x-frame-options")
        if not xfo and (not csp or "frame-ancestors" not in csp):
            findings.append(SecurityHeaderFinding(
                header_name="X-Frame-Options",
                status="FAIL",
                severity=IndicatorSeverity.MEDIUM,
                value=None,
                impact="Allows the page to be embedded in malicious iframes (Clickjacking).",
                remediation="Add X-Frame-Options: DENY or SAMEORIGIN, or CSP frame-ancestors 'self'."
            ))
        else:
            findings.append(SecurityHeaderFinding(
                header_name="X-Frame-Options",
                status="PASS",
                severity=IndicatorSeverity.INFO,
                value=xfo or "Covered by CSP frame-ancestors",
                impact="Protects interface from iframe overlay and Clickjacking attacks.",
                remediation="Maintain configuration."
            ))

        # 4. X-Content-Type-Options
        xcto = headers.get("x-content-type-options")
        if not xcto or "nosniff" not in xcto.lower():
            findings.append(SecurityHeaderFinding(
                header_name="X-Content-Type-Options",
                status="FAIL",
                severity=IndicatorSeverity.LOW,
                value=xcto,
                impact="Browser may perform MIME-type sniffing, treating non-executable files as scripts or stylesheets.",
                remediation="Add X-Content-Type-Options: nosniff"
            ))
        else:
            findings.append(SecurityHeaderFinding(
                header_name="X-Content-Type-Options",
                status="PASS",
                severity=IndicatorSeverity.INFO,
                value=xcto,
                impact="Prevents MIME-confusion attacks.",
                remediation="Maintain configuration."
            ))

        # 5. Information Disclosure (Server / X-Powered-By)
        server = headers.get("server")
        x_powered_by = headers.get("x-powered-by")
        if server and any(c.isdigit() for c in server):
            findings.append(SecurityHeaderFinding(
                header_name="Server Header Leak",
                status="WARN",
                severity=IndicatorSeverity.LOW,
                value=server,
                impact=f"Exposes exact web server software version '{server}', simplifying vulnerability reconnaissance.",
                remediation="Obfuscate or disable detailed Server tokens in web server configuration."
            ))
        if x_powered_by:
            findings.append(SecurityHeaderFinding(
                header_name="X-Powered-By Leak",
                status="WARN",
                severity=IndicatorSeverity.LOW,
                value=x_powered_by,
                impact=f"Discloses application runtime technology '{x_powered_by}'.",
                remediation="Remove X-Powered-By header from backend framework settings."
            ))

        # 6. Referrer-Policy
        ref_pol = headers.get("referrer-policy")
        if not ref_pol:
            findings.append(SecurityHeaderFinding(
                header_name="Referrer-Policy",
                status="WARN",
                severity=IndicatorSeverity.LOW,
                value=None,
                impact="Referer URLs containing query parameters or session IDs may leak to third-party endpoints.",
                remediation="Add Referrer-Policy: strict-origin-when-cross-origin"
            ))
        else:
            findings.append(SecurityHeaderFinding(
                header_name="Referrer-Policy",
                status="PASS",
                severity=IndicatorSeverity.INFO,
                value=ref_pol,
                impact="Restricts leakage of path and query data across origins.",
                remediation="Maintain configuration."
            ))

        return findings
