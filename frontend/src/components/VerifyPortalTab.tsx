import React, { useState } from 'react';
import { FileCheck, ShieldCheck, Search, AlertCircle, Copy, Check, ArrowRight, Lock } from 'lucide-react';

interface VerifyPortalTabProps {
  initialHash?: string;
}

export const VerifyPortalTab: React.FC<VerifyPortalTabProps> = ({ initialHash }) => {
  const [reportHash, setReportHash] = useState(initialHash || '');
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleVerify = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!reportHash.trim()) return;

    setIsVerifying(true);
    setError(null);
    setVerificationResult(null);

    try {
      const res = await fetch(`/api/blockchain/verify/${encodeURIComponent(reportHash.trim())}`);
      if (!res.ok) {
        throw new Error(`Report commitment not found on-chain. Status: ${res.status}`);
      }
      const data = await res.json();
      setVerificationResult(data);
    } catch (err: any) {
      setError(err.message || 'Verification failed');
    } finally {
      setIsVerifying(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">

      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 space-y-2">
        <div className="flex items-center space-x-2">
          <FileCheck className="w-5 h-5 text-amber-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Independent Decentralized Threat Report Verifier
          </h3>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          Verify the cryptographic integrity and provenance of any AegisTrust threat report directly against the EVM 
          <code className="text-amber-300 mx-1">ThreatReportRegistry.sol</code> smart contract. 
          Mathematical commitments ensure reports cannot be retroactively modified, censored, or forged.
        </p>
      </div>

      {/* Query Form */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 shadow-2xl">
        <form onSubmit={handleVerify} className="space-y-4">
          <label className="block text-xs font-mono uppercase tracking-wider text-slate-400">
            Report Commitment Hash (Keccak-256)
          </label>
          <div className="relative flex items-center">
            <Search className="absolute left-4 w-5 h-5 text-slate-400 pointer-events-none" />
            <input
              type="text"
              value={reportHash}
              onChange={(e) => setReportHash(e.target.value)}
              placeholder="Enter Keccak-256 hash (e.g., 0x9a8f4c...)"
              className="w-full pl-12 pr-32 py-4 rounded-xl bg-slate-950/90 border border-white/10 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-amber-500 font-mono transition-all"
            />
            <button
              type="submit"
              disabled={isVerifying || !reportHash.trim()}
              className="absolute right-2 px-6 py-2.5 rounded-lg bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500 text-black font-bold text-xs uppercase tracking-wider transition-all disabled:opacity-50 flex items-center space-x-2"
            >
              {isVerifying ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-black border-t-transparent rounded-full animate-spin" />
                  <span>Verifying...</span>
                </>
              ) : (
                <>
                  <span>Verify</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Error View */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-950/50 border border-rose-500/50 text-xs text-rose-300 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Valid Verification Result Card */}
      {verificationResult && (
        <div className="p-6 rounded-2xl bg-slate-900/90 border border-amber-500/40 cyber-glow-amber space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-white/10">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                  Cryptographic Integrity Confirmed
                </h4>
                <p className="text-xs text-emerald-400 font-mono">
                  100% Match with On-Chain Ledger Commitment
                </p>
              </div>
            </div>

            <span className="text-xs font-mono uppercase px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">
              TAMPER-PROOF
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-500 block uppercase">Report Commitment Hash</span>
              <div className="flex items-center justify-between">
                <span className="text-amber-300 truncate mr-2">{verificationResult.details.report_hash}</span>
                <button
                  onClick={() => copyToClipboard(verificationResult.details.report_hash)}
                  className="p-1 hover:text-white"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                </button>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-500 block uppercase">Indicator Digest (Target Hash)</span>
              <span className="text-slate-300 truncate block">{verificationResult.details.indicator_hash}</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-500 block uppercase">Notarized Risk Level</span>
              <span className="text-rose-400 font-bold">{verificationResult.details.risk_class} (Score: {verificationResult.details.risk_score}/100)</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-500 block uppercase">Anchored Timestamp</span>
              <span className="text-slate-300">
                {new Date(verificationResult.details.timestamp * 1000).toUTCString()}
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-500 block uppercase">Submitter Oracle Address</span>
              <span className="text-purple-300 truncate block">{verificationResult.details.reporter}</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-500 block uppercase">Network Provenance</span>
              <span className="text-cyan-300 truncate block">{verificationResult.details.network}</span>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-white/5 text-xs text-slate-400 space-y-2">
            <div className="flex items-center space-x-1.5 text-slate-300 font-semibold">
              <Lock className="w-4 h-4 text-amber-400" />
              <span>Zero-PII Compliance & Cryptographic Integrity Guarantee</span>
            </div>
            <p className="leading-relaxed">
              Raw URLs, personal communications, and sensitive passwords are never broadcast onto public blockchains. 
              The on-chain Keccak-256 mathematical hash mathematically proves that the exact forensic report held locally 
              existed in its current form at the indicated timestamp without single-byte manipulation.
            </p>
          </div>
        </div>
      )}

    </div>
  );
};
