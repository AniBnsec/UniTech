import re
import unicodedata
from typing import Optional, Tuple, List, Dict

# Catalog of highly-targeted brands and legitimate domains
TARGETED_BRANDS: Dict[str, List[str]] = {
    "paypal": ["paypal.com", "paypal.me"],
    "chase": ["chase.com"],
    "bankofamerica": ["bankofamerica.com", "bofa.com"],
    "wellsfargo": ["wellsfargo.com"],
    "sbi": ["onlinesbi.sbi", "sbi.co.in"],
    "hdfcbank": ["hdfcbank.com"],
    "icicibank": ["icicibank.com"],
    "microsoft": ["microsoft.com", "live.com", "office.com", "login.microsoftonline.com"],
    "apple": ["apple.com", "icloud.com"],
    "google": ["google.com", "accounts.google.com", "gmail.com"],
    "amazon": ["amazon.com", "amazon.in", "amazon.co.uk"],
    "netflix": ["netflix.com"],
    "binance": ["binance.com"],
    "coinbase": ["coinbase.com"],
    "metamask": ["metamask.io"],
    "kraken": ["kraken.com"],
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"],
    "linkedin": ["linkedin.com"],
    "dhl": ["dhl.com", "dhl.de"],
    "fedex": ["fedex.com"],
    "usps": ["usps.com"],
    "internal revenue service": ["irs.gov"],
    "income tax": ["incometax.gov.in"],
    "telegram": ["telegram.org", "t.me"],
    "whatsapp": ["whatsapp.com"],
    "zoom": ["zoom.us"],
    "dropbox": ["dropbox.com"],
}

HOMOGLYPH_MAP: Dict[str, str] = {
    'а': 'a', 'á': 'a', 'ä': 'a', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'å': 'a', 'ɑ': 'a', 'α': 'a',
    'с': 'c', 'ç': 'c', 'ć': 'c', 'č': 'c',
    'е': 'e', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'е́': 'e', 'ε': 'e',
    'і': 'i', 'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i', 'ι': 'i', 'ı': 'i',
    'ј': 'j',
    'к': 'k', 'κ': 'k',
    'о': 'o', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ο': 'o', '0': 'o',
    'р': 'p', 'ρ': 'p',
    'ѕ': 's', 'ş': 's', 'š': 's',
    'у': 'y', 'ý': 'y', 'ÿ': 'y',
    'х': 'x', 'χ': 'x',
    'v': 'v', 'ν': 'v',
    'w': 'w', 'ω': 'w',
    'ԁ': 'd', 'q': 'q', 'b': 'b',
}

SUSPICIOUS_TLDS = {
    "xyz", "top", "work", "loan", "click", "buzz", "gq", "cf", "ml", "ga", "tk",
    "fit", "live", "rest", "surf", "monster", "hair", "beauty", "quest", "cfd", "sbs"
}

SUSPICIOUS_KEYWORD_PATTERNS = [
    r"login", r"signin", r"verify", r"update", r"secure", r"security", r"account",
    r"banking", r"confirm", r"password", r"credential", r"wallet", r"support",
    r"recovery", r"auth", r"token", r"portal", r"billing", r"tax", r"refund",
    r"kyc", r"otp", r"session", r"unblock", r"claim"
]

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates classic Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def normalize_homoglyphs(text: str) -> Tuple[str, bool]:
    """Normalizes lookalike Unicode characters to standard ASCII."""
    has_homoglyphs = False
    result = []
    
    for char in text.lower():
        if char in HOMOGLYPH_MAP:
            result.append(HOMOGLYPH_MAP[char])
            has_homoglyphs = True
        else:
            decomposed = unicodedata.normalize('NFKD', char)
            ascii_char = decomposed.encode('ASCII', 'ignore').decode('ASCII')
            if ascii_char and ascii_char != char:
                has_homoglyphs = True
                result.append(ascii_char)
            else:
                result.append(char)
                
    return "".join(result), has_homoglyphs

def detect_typosquatting(domain: str) -> Optional[Dict[str, any]]:
    """
    Analyzes whether a domain is typosquatting or impersonating a known brand across:
    1. Entire domain labels
    2. Tokenized sub-labels (e.g. 'paypai-security' -> 'paypai')
    3. Homoglyph character substitution
    """
    clean_domain = domain.lower().strip()
    
    parts = clean_domain.split('.')
    main_label = parts[-2] if len(parts) >= 2 else clean_domain
    normalized_label, had_homoglyphs = normalize_homoglyphs(main_label)
    tokens = re.split(r'[-_]', normalized_label)

    for brand, legits in TARGETED_BRANDS.items():
        # Check if legitimate domain directly
        if clean_domain in legits or any(clean_domain.endswith("." + l) for l in legits):
            return None
            
        # 1. Exact homoglyph match
        if had_homoglyphs and (normalized_label == brand or brand in tokens):
            return {
                "brand": brand,
                "type": "Homoglyph Attack",
                "details": f"The domain uses visual Unicode lookalikes (homoglyphs) to deceptively mimic {brand} ({legits[0]}).",
                "legitimate_domain": legits[0],
                "severity": "CRITICAL"
            }
            
        # 2. Check brand embedding with phishing keywords
        if brand in normalized_label and normalized_label != brand:
            has_kw = any(re.search(kw, normalized_label) for kw in SUSPICIOUS_KEYWORD_PATTERNS)
            return {
                "brand": brand,
                "type": "Brand Impersonation / Keyword Stuffing",
                "details": f"Targeted brand '{brand}' embedded in domain '{clean_domain}' alongside suspicious keywords.",
                "legitimate_domain": legits[0],
                "severity": "HIGH" if has_kw else "MEDIUM"
            }

        # 3. Levenshtein distance on main label OR any sub-token
        labels_to_check = [normalized_label] + tokens
        for candidate in labels_to_check:
            if len(candidate) < 3:
                continue
            dist = levenshtein_distance(candidate, brand)
            if 1 <= dist <= 2 and len(brand) >= 4 and abs(len(candidate) - len(brand)) <= 2:
                return {
                    "brand": brand,
                    "type": "Typosquatting",
                    "details": f"The domain token '{candidate}' differs by only {dist} edit(s) from authentic brand '{brand}' ({legits[0]}).",
                    "legitimate_domain": legits[0],
                    "distance": dist,
                    "severity": "HIGH"
                }

    return None
