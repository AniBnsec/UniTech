# AegisTrust: AI-Powered Web Threat Detection & Digital Trust Intelligence

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Solidity](https://img.shields.io/badge/solidity-^0.8.20-363636.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)]()
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **AegisTrust** is an accessible, unified digital security platform that synthesizes **Artificial Intelligence**, **Cybersecurity Engineering**, and **Web3 Decentralized Trust** to detect phishing websites, deceptive communications, and digital certificate trust failures before individuals and organizations fall victim.

---

## 1. Real-World Problem & Incident Context

1. **The "HTTPS = Safe" Fallacy:** Modern users mistakenly treat the browser padlock as a seal of legitimacy. Attackers readily issue automated, valid TLS certificates for phishing sites targeting banks, universities, and government portals.
2. **The eMudhra TLS Incident & Cryptographic Trust Fragility:** Weaknesses in Certificate Authority (CA) key generation can undermine the entire web's trust chain. AegisTrust explicitly audits intermediate trust chains, detecting certificates minted under compromised or distrusted CA hierarchies (such as the eMudhra sub-CA action and historical precedents).
3. **Multi-Vector Social Engineering:** Scams exploit human cognitive biases—urgency, authority impersonation, and financial bait—across SMS, email, and social messaging.
4. **Decentralized Verification vs. Siloed Blacklists:** Centralized blocklists can be tampered with or censored. AegisTrust anchors cryptographic commitments (`Keccak-256`) of threat reports into an EVM smart contract, guaranteeing tamper-evident provenance while preserving 100% off-chain privacy for sensitive user data.

---

## 2. Platform Architecture & Modules

```
                           ┌──────────────────────────────────────────────┐
                           │            AegisTrust Command UI             │
                           │   (Next.js / React + Tailwind CSS + Lucide)  │
                           └──────────────────────┬───────────────────────┘
                                                  │ REST / JSON
                                                  ▼
                           ┌──────────────────────────────────────────────┐
                           │             FastAPI Core Gateway             │
                           └───────┬──────────────┬──────────────┬────────┘
                                   │              │              │
             ┌─────────────────────┘              │              └─────────────────────┐
             ▼                                    ▼                                    ▼
┌─────────────────────────┐          ┌─────────────────────────┐          ┌─────────────────────────┐
│   Cybersecurity Core    │          │     AI Scam Engine      │          │    Web3 Trust Layer     │
├─────────────────────────┤          ├─────────────────────────┤          ├─────────────────────────┤
│ • Punycode & Homoglyphs │          │ • 5-Factor Coercion     │          │ • ThreatReportRegistry  │
│ • Typosquatting (Dist 2)│          │ • Linguistic Heuristics │          │ • Keccak-256 Hashes     │
│ • SSRF-Safe Redirects   │          │ • IOC Extraction (BTC)  │          │ • Zero-PII Compliance   │
│ • eMudhra CA Trust Audit│          │ • Plain-English Rationale│         │ • Public Verifier       │
│ • Passive Header Checks │          │ • Gemini LLM Dual-Mode  │          │ • EVM / Hardhat         │
└─────────────────────────┘          └─────────────────────────┘          └─────────────────────────┘
```

### Module Breakdown
- **Module 1: Intelligent URL & Domain Analysis:** Detects Punycode IDN homoglyphs (Cyrillic lookalikes), computes Levenshtein brand distance across 120+ targeted brands, inspects Shannon entropy, and tracks HTTP redirects with SSRF protection (blocking RFC1918 and AWS metadata `169.254.169.254`).
- **Module 2: TLS Certificate & Digital Trust Analysis:** Low-level X.509 handshake inspection, SAN matching, signature algorithm evaluation, public key bit-length audits, and cross-referencing against the **eMudhra & Distrusted CA Database**.
- **Module 3: AI-Powered Scam & Message Analysis:** 5-factor psychological coercion scoring (Urgency, Financial Bait, Authority, Credential/OTP Solicitation, Isolation). Automatically extracts crypto deposit addresses (BTC, ETH, Tron), contact vectors, and impersonated institutions.
- **Module 4: Intelligent Threat Correlation:** Graph engine clustering shared IP subnets, bulletproof hosts, compromised CAs, and reused cryptocurrency mule wallets across incidents.
- **Module 5: Passive Website Security Assessment:** Safe, zero-exploitation HTTP header audit evaluating CSP, HSTS, X-Frame-Options, MIME sniffing protection, and server header disclosures.
- **Module 6: Decentralized Threat Intelligence (Web3):** Solidity smart contract (`ThreatReportRegistry.sol`) anchoring cryptographic hashes of threat reports on EVM networks. Independent verifier portal allows anyone to mathematically prove report integrity without central authority.

---

## 3. Evaluation Criteria Mapping

| Challenge Dimension | Weight | AegisTrust Implementation |
| :--- | :---: | :--- |
| **Cybersecurity & Threat Detection** | **30%** | Comprehensive X.509 chain auditor with dedicated **eMudhra CA incident** detection, Levenshtein typosquatting scanner (120+ brands), Punycode homoglyph decoder, and SSRF-safe redirect tracer. |
| **AI Implementation** | **20%** | 5-factor psychological coercion matrix, multi-IOC regex/NLP extraction (wallets, URLs, phones), and evidence-grounded non-hallucinatory explanations with explicit limitations. |
| **Web3 Integration** | **20%** | Production-grade `ThreatReportRegistry.sol` smart contract, Keccak-256 report hash commitments, independent on-chain verification portal, and strict zero-PII privacy enforcement. |
| **Technical Implementation** | **20%** | Decoupled modern architecture: Python 3.14 FastAPI + React Vite Tailwind + Hardhat EVM suite with 100% passing automated test suite. |
| **Innovation & User Experience** | **10%** | Cyber Operations Center aesthetic with dark mode, interactive topology threat graph, and a **1-click Judge Demonstration Bar** with 6 pre-configured test cases. |

---

## 4. Quick Start Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ (Tested on Node 24)
- npm 9+

### 1. Verify the Entire System
Run the unified test suite to execute Pytest, Hardhat, and Vite checks:
```bash
python verify_system.py
```

### 2. Start Backend API Server
```powershell
# Activate Python Virtual Environment
.\venv\Scripts\activate

# Launch FastAPI Server
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: **http://127.0.0.1:8000/docs**

### 3. Start Frontend Dashboard
In a separate terminal:
```bash
cd frontend
npm run dev
```
Interactive UI will be live at: **http://localhost:3000**

---

## 5. Judge Demonstration Suite (6 Pre-Configured Scenarios)

The AegisTrust Dashboard features a **1-Click Demo Bar** at the top of the interface for instantaneous live evaluation:

### Malicious Scenarios
1. **Brand Typosquatting (PayPal):** `https://paypaI-security-update.com/login?token=8923`
   - *Indicators:* Levenshtein typosquatting match, homoglyph characters, suspicious keywords (`login`, `security`), threat feed match.
   - *Verdict:* `Confirmed Malicious` (Score: 92/100).
2. **eMudhra Compromised CA Incident Simulator:** `https://emudhra-test.unitech-demo.local/login`
   - *Indicators:* Flagged intermediate CA under active distrust notices, cryptographic key-generation vulnerability, expired cert.
   - *Verdict:* `Confirmed Malicious` (Demonstrates HTTPS ≠ Safe).
3. **SMS Banking & Crypto Scam Message:**
   - *Input:* `"URGENT: SBI Account suspended due to missing KYC! Within 24 hours, click https://sbi-kyc-update-pan.top or deposit 0.05 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. Share your 6-digit OTP code immediately."`
   - *Indicators:* Urgency score (100/100), Credential/OTP harvesting (70/100), BTC address extraction, malicious URL.
   - *Verdict:* `Confirmed Malicious` (Score: 85/100).

### Benign Scenarios (Ground Truth)
4. **State Bank of India (Official Portal):** `https://www.onlinesbi.sbi`
   - *Verdict:* `Low Risk` (Valid EV certificate, official government-backed TLD, zero threat flags).
5. **Microsoft Enterprise Portal:** `https://www.microsoft.com`
   - *Verdict:* `Low Risk` (Strict HSTS preload, verified DigiCert trust chain, clean domain reputation).
6. **University of Oxford Portal:** `https://www.ox.ac.uk`
   - *Verdict:* `Low Risk` (Accredited academic TLD, legitimate X.509 hierarchy).

---

## 6. Smart Contract Architecture (`ThreatReportRegistry.sol`)

The Solidity contract is compiled and tested with Hardhat (`solc 0.8.20`):

```solidity
struct ThreatReport {
    bytes32 reportHash;           // Keccak-256 of canonical report JSON
    bytes32 indicatorHash;        // Keccak-256 of normalized domain/indicator
    RiskClassification riskClass; // LowRisk, Suspicious, HighRisk, ConfirmedMalicious, Inconclusive
    uint8 riskScore;              // 0 to 100
    uint64 timestamp;             // Block timestamp
    address reporter;             // Submitter wallet address
    ReportStatus status;          // Active, Verified, Disputed, Revoked
    uint32 verificationCount;     // Independent peer attestations
    uint32 disputeCount;          // Community disputes
    string ipfsCid;               // Optional encrypted archive reference
}
```

### Running Smart Contract Unit Tests
```bash
cd contracts
npx hardhat test
```
**Results:** `7 passing tests` covering report registration, duplicate prevention, risk score bounds, peer attestations, dispute handling, reporter-exclusive revocation, and independent integrity verification.

---

## 7. Security & Privacy Guarantees

- **SSRF Defense:** Dedicated socket resolver verifies target IPs before HTTP connection, explicitly dropping private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), loopback (`127.0.0.0/8`), and cloud metadata (`169.254.169.254`).
- **Passive Inspection Policy:** AegisTrust never executes untrusted JavaScript in an unsandboxed browser and never downloads executable binary files.
- **Zero-PII On-Chain Guarantee:** Raw URLs, victim emails, personal credentials, and message bodies are strictly prohibited from blockchain storage. Only irreversible mathematical hashes (`keccak256`) and category enumerations are anchored.

---

## 8. License
This project is open-source under the [MIT License](LICENSE).
