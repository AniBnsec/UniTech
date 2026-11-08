import React, { useState } from 'react';
import { URLScanResult, ThreatIndicator, IndicatorSeverity } from '../types';
import { 
  Search, ShieldAlert, ShieldCheck, AlertTriangle, Lock, Unlock, 
  ExternalLink, Layers, ArrowRight, CheckCircle2, XCircle, 
  Cpu, Award, Copy, Check, Info, FileCode2
} from 'lucide-react';

interface UrlScannerTabProps {
  onScan: (url: string, allowRedirects: boolean, recordOnChain: boolean) => Promise<void>;
  scanResult: URLScanResult | null;
  isLoading: boolean;
  onVerifyHash: (hash: string) => void;
  targetUrl: string;
  setTargetUrl: (url: string) => void;
}

export const UrlScannerTab: React.FC<UrlScannerTabProps> = ({
  onScan,
  scanResult,
  isLoading,
  onVerifyHash,
  targetUrl,
  setTargetUrl
}) => {
  const [allowRedirects, setAllowRedirects] = useState(true);
  const [recordOnChain, setRecordOnChain] = useState(true);
  const [copiedHash, setCopiedHash] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetUrl.trim() || isLoading) return;
    onScan(targetUrl.trim(), allowRedirects, recordOnChain);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedHash(true);
    setTimeout(() => setCopiedHash(false), 2000);
  };

  const getRiskColor = (score: number, classification: string) => {
    if (classification === 'Confirmed Malicious' || score >= 80) return 'text-rose-400 bg-rose-950/40 border-rose-500/40';
    if (classification === 'High Risk' || score >= 55) return 'text-orange-400 bg-orange-950/40 border-orange-500/40';
    if (classification === 'Suspicious' || score >= 21) return 'text-amber-400 bg-amber-950/40 border-amber-500/40';
    return 'text-emerald-400 bg-emerald-950/40 border-emerald-500/40';
  };

  const getSeverityBadge = (sev: IndicatorSeverity) => {
    switch (sev) {
      case 'CRITICAL': return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'HIGH': return 'bg-orange-500/20 text-orange-300 border-orange-500/40';
      case 'MEDIUM': return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      case 'LOW': return 'bg-blue-500/20 text-blue-300 border-blue-500/40';
      default: return 'bg-slate-500/20 text-slate-300 border-slate-500/40';
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Search & Configuration Bar */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 shadow-2xl">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative flex items-center">
            <Search className="absolute left-4 w-5 h-5 text-slate-400 pointer-events-none" />
            <input
              type="text"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              placeholder="Enter suspicious URL or domain (e.g., https://paypaI-security.com or https://onlinesbi.sbi)"
              className="w-full pl-12 pr-32 py-4 rounded-xl bg-slate-950/90 border border-white/10 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 font-mono transition-all"
            />
            <button
              type="submit"
              disabled={isLoading || !targetUrl.trim()}
              className="absolute right-2 px-6 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black font-bold text-xs uppercase tracking-wider transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-black border-t-transparent rounded-full animate-spin" />
                  <span>Scanning...</span>
                </>
              ) : (
                <>
                  <span>Investigate</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400 pt-1">
            <div className="flex items-center space-x-6">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={allowRedirects}
                  onChange={(e) => setAllowRedirects(e.target.checked)}
                  className="rounded bg-slate-800 border-slate-700 text-cyan-500 focus:ring-0"
                />
                <span>Safe Redirect Tracing (SSRF-Guarded)</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={recordOnChain}
                  onChange={(e) => setRecordOnChain(e.target.checked)}
                  className="rounded bg-slate-800 border-slate-700 text-cyan-500 focus:ring-0"
                />
                <span className="text-cyan-400 font-medium">Record Cryptographic Proof On-Chain (Web3)</span>
              </label>
            </div>

            <div className="flex items-center space-x-2 font-mono text-[11px] text-slate-500">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
              <span>Passive Probing Only (Zero Exploitation)</span>
            </div>
          </div>
        </form>
      </div>

      {/* Loading Stepper Animation */}
      {isLoading && (
        <div className="p-8 rounded-2xl bg-slate-900/60 border border-cyan-500/30 text-center space-y-4 animate-pulse">
          <div className="w-12 h-12 mx-auto rounded-full bg-cyan-500/20 flex items-center justify-center text-cyan-400">
            <Cpu className="w-6 h-6 animate-spin" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider">Executing Multi-Vector Security Inspection</h4>
            <p className="text-xs text-slate-400 mt-1">Inspecting Punycode & Typosquatting → Tracing Redirects → Auditing TLS & eMudhra CA Trust → Generating On-Chain Commitment</p>
          </div>
        </div>
      )}

      {/* Investigation Results */}
      {scanResult && !isLoading && (
        <div className="space-y-6">

          {/* Primary Risk & Executive Verdict Card */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 cyber-border">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-white/10">
              
              <div className="flex items-start space-x-4">
                <div className={`p-4 rounded-2xl border ${getRiskColor(scanResult.risk_score, scanResult.risk_classification)} flex flex-col items-center justify-center min-w-[90px]`}>
                  <span className="text-2xl font-black font-mono">{scanResult.risk_score}</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider">Risk Score</span>
                </div>
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-extrabold uppercase border ${getRiskColor(scanResult.risk_score, scanResult.risk_classification)}`}>
                      {scanResult.risk_classification}
                    </span>
                    <span className="text-xs font-mono text-slate-400">
                      Confidence: {(scanResult.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mt-1">{scanResult.summary_verdict}</h3>
                  <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
                    {scanResult.executive_explanation}
                  </p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row lg:flex-col gap-2 font-mono text-xs">
                <div className="px-3 py-2 rounded-xl bg-slate-950/80 border border-white/5">
                  <span className="text-slate-500 block text-[10px] uppercase">Domain</span>
                  <span className="text-cyan-300 font-semibold">{scanResult.domain}</span>
                </div>
                {scanResult.ip_address && (
                  <div className="px-3 py-2 rounded-xl bg-slate-950/80 border border-white/5">
                    <span className="text-slate-500 block text-[10px] uppercase">Resolved IP</span>
                    <span className="text-slate-300">{scanResult.ip_address}</span>
                  </div>
                )}
              </div>

            </div>

            {/* Special Highlight: eMudhra Compromised CA Incident Alert */}
            {scanResult.certificate?.is_compromised_ca && (
              <div className="mt-4 p-4 rounded-xl bg-rose-950/60 border border-rose-500/60 flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
                <div className="text-xs">
                  <div className="font-bold text-rose-200 uppercase tracking-wide">
                    eMudhra Sub-CA Distrust / Compromised Trust Action Detected
                  </div>
                  <p className="text-rose-300/90 mt-1 leading-relaxed">
                    {scanResult.certificate.ca_incident_notes || "The certificate authority key generation weakness matches public distrust notices. Even though HTTPS is configured, domain authenticity cannot be trusted."}
                  </p>
                </div>
              </div>
            )}

            {/* Recommended Precautions */}
            {scanResult.recommended_precautions.length > 0 && (
              <div className="mt-4 pt-4 border-t border-white/5">
                <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2">Recommended Actions & Precautions</h5>
                <ul className="space-y-1 text-xs text-slate-300">
                  {scanResult.recommended_precautions.map((p, idx) => (
                    <li key={idx} className="flex items-center space-x-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Technical Threat Indicators Breakdown */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 text-cyan-400" />
                <span>Identified Threat Indicators ({scanResult.indicators.length})</span>
              </h4>
              <span className="text-xs text-slate-400 font-mono">Evidence-Grounded Signals</span>
            </div>

            {scanResult.indicators.length === 0 ? (
              <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-800/30 text-emerald-300 text-xs flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>No malicious technical indicators detected in domain structure, redirects, or certificate.</span>
              </div>
            ) : (
              <div className="space-y-3">
                {scanResult.indicators.map((ind, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-950/80 border border-white/5 space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getSeverityBadge(ind.severity)}`}>
                          {ind.severity}
                        </span>
                        <span className="text-xs font-semibold text-white">{ind.title}</span>
                      </div>
                      <span className="text-[11px] font-mono text-slate-400">{ind.category}</span>
                    </div>

                    <div className="text-xs font-mono text-cyan-300/90 bg-cyan-950/30 px-3 py-1.5 rounded-lg border border-cyan-800/30">
                      <strong>Evidence:</strong> {ind.evidence}
                    </div>

                    <p className="text-xs text-slate-400 leading-relaxed">
                      {ind.description}
                    </p>

                    {ind.mitigation && (
                      <div className="text-[11px] text-amber-300/80 flex items-center space-x-1.5 pt-1">
                        <Info className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
                        <span><strong>Mitigation:</strong> {ind.mitigation}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Dual Grid: TLS Certificate Audit & Passive Security Headers */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* TLS & Web Trust Card */}
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                  <Lock className="w-4 h-4 text-cyan-400" />
                  <span>TLS Certificate & Digital Trust</span>
                </h4>
                {scanResult.certificate?.is_expired ? (
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                    Expired
                  </span>
                ) : scanResult.certificate ? (
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                    Active TLS
                  </span>
                ) : (
                  <span className="text-[10px] text-slate-400">No TLS Handshake</span>
                )}
              </div>

              {scanResult.certificate ? (
                <div className="space-y-3 font-mono text-xs">
                  <div className="p-3 rounded-xl bg-slate-950/70 border border-white/5 space-y-1.5">
                    <div className="text-slate-400 text-[11px]">Issuer Organization & CN:</div>
                    <div className="text-white font-semibold">
                      {scanResult.certificate.issuer_org || scanResult.certificate.issuer_cn || "Unknown Issuer"}
                    </div>
                    {scanResult.certificate.is_compromised_ca && (
                      <div className="text-[11px] text-rose-400 font-bold">
                        ⚠️ Distrusted intermediate CA hierarchy
                      </div>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div className="p-2.5 rounded-lg bg-slate-950/50 border border-white/5">
                      <span className="text-slate-500 block">Public Key</span>
                      <span className="text-slate-200">
                        {scanResult.certificate.public_key_type} ({scanResult.certificate.public_key_bits}-bit)
                      </span>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-950/50 border border-white/5">
                      <span className="text-slate-500 block">Algorithm</span>
                      <span className="text-slate-200">{scanResult.certificate.signature_algorithm || "SHA-256"}</span>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-950/50 border border-white/5">
                      <span className="text-slate-500 block">Expires In</span>
                      <span className={scanResult.certificate.days_until_expiration && scanResult.certificate.days_until_expiration < 0 ? "text-rose-400" : "text-slate-200"}>
                        {scanResult.certificate.days_until_expiration} days
                      </span>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-950/50 border border-white/5">
                      <span className="text-slate-500 block">Cert Transparency (CT)</span>
                      <span className="text-emerald-400">
                        {scanResult.certificate.certificate_transparency_present ? "SCT Embedded" : "Missing SCT"}
                      </span>
                    </div>
                  </div>

                  {scanResult.certificate.subject_alt_names.length > 0 && (
                    <div className="p-2.5 rounded-lg bg-slate-950/50 border border-white/5 text-[11px]">
                      <span className="text-slate-500 block mb-1">Subject Alternative Names (SANs):</span>
                      <div className="text-slate-300 break-all max-h-16 overflow-y-auto">
                        {scanResult.certificate.subject_alt_names.slice(0, 5).join(", ")}
                      </div>
                    </div>
                  )}

                  <div className="p-2.5 rounded-lg bg-cyan-950/20 border border-cyan-800/30 text-[11px] text-cyan-300">
                    <strong>Golden Rule:</strong> HTTPS ensures encrypted transport and host identity verification. It does not validate absence of phishing or fraud.
                  </div>
                </div>
              ) : (
                <div className="p-6 rounded-xl bg-slate-950/60 border border-white/5 text-center text-xs text-slate-400">
                  Target host did not present a standard TLS/HTTPS certificate.
                </div>
              )}
            </div>

            {/* Passive Security Headers Card */}
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                  <FileCode2 className="w-4 h-4 text-cyan-400" />
                  <span>Passive Security Headers Audit</span>
                </h4>
                <span className="text-xs font-mono text-slate-400">Non-Intrusive</span>
              </div>

              <div className="space-y-2.5 max-h-[350px] overflow-y-auto pr-1">
                {scanResult.security_headers.map((h, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-white/5 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-semibold text-white">{h.header_name}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        h.status === 'PASS' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                        h.status === 'WARN' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                        'bg-rose-950 text-rose-300 border border-rose-800'
                      }`}>
                        {h.status}
                      </span>
                    </div>

                    <p className="text-[11px] text-slate-400 leading-normal">
                      {h.impact}
                    </p>

                    {h.status !== 'PASS' && (
                      <div className="text-[10px] font-mono text-cyan-300/80 bg-slate-900 p-2 rounded border border-white/5 mt-1">
                        <strong>Fix:</strong> {h.remediation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* Web3 On-Chain Cryptographic Proof Card */}
          {scanResult.on_chain_proof && (
            <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900/90 via-cyan-950/20 to-slate-900/90 border border-cyan-500/40 cyber-glow-blue space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Award className="w-5 h-5 text-cyan-400" />
                  <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                    Decentralized Threat Intelligence Proof (Web3)
                  </h4>
                </div>
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-cyan-900/50 text-cyan-300 border border-cyan-700/50">
                  Tamper-Evident Provenance
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">
                A cryptographic commitment of this report has been anchored on-chain using <strong>Keccak-256</strong>. 
                In compliance with privacy standards, zero raw URLs, victim credentials, or personal identifiers are stored on-chain.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-xs">
                <div className="p-3 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-500 block uppercase">Report Commitment Hash (Keccak-256)</span>
                  <div className="flex items-center justify-between">
                    <span className="text-cyan-300 truncate mr-2">{scanResult.on_chain_proof.report_hash}</span>
                    <button
                      onClick={() => copyToClipboard(scanResult.on_chain_proof!.report_hash)}
                      className="p-1.5 rounded hover:bg-white/10 text-slate-400 hover:text-white"
                      title="Copy Hash"
                    >
                      {copiedHash ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-500 block uppercase">Smart Contract Registry Address</span>
                  <span className="text-slate-300 truncate block">{scanResult.on_chain_proof.contract_address}</span>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-500 block uppercase">Transaction Hash</span>
                  <span className="text-emerald-400 truncate block">{scanResult.on_chain_proof.tx_hash}</span>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-500 block uppercase">Attestation Oracle</span>
                  <span className="text-purple-300 truncate block">{scanResult.on_chain_proof.reporter}</span>
                </div>
              </div>

              <div className="flex items-center justify-end pt-2">
                <button
                  onClick={() => onVerifyHash(scanResult.on_chain_proof!.report_hash)}
                  className="px-4 py-2 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                >
                  <span>Verify Report Independently in Web3 Portal</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  );
};

