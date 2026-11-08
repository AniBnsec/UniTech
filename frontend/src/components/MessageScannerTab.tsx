import React, { useState } from 'react';
import { MessageScanResult, IndicatorSeverity } from '../types';
import { 
  Cpu, AlertTriangle, ShieldCheck, ArrowRight, Wallet, 
  Phone, Link as LinkIcon, Building2, CheckCircle2, Copy, Check, Info 
} from 'lucide-react';

interface MessageScannerTabProps {
  onScanMessage: (text: string, channel: string) => Promise<void>;
  messageResult: MessageScanResult | null;
  isLoading: boolean;
  messageText: string;
  setMessageText: (text: string) => void;
  onVerifyHash: (hash: string) => void;
}

export const MessageScannerTab: React.FC<MessageScannerTabProps> = ({
  onScanMessage,
  messageResult,
  isLoading,
  messageText,
  setMessageText,
  onVerifyHash
}) => {
  const [channel, setChannel] = useState('sms');
  const [copiedText, setCopiedText] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageText.trim() || isLoading) return;
    onScanMessage(messageText.trim(), channel);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedText(text);
    setTimeout(() => setCopiedText(null), 2000);
  };

  const getCoercionBarColor = (score: number) => {
    if (score >= 70) return 'bg-rose-500';
    if (score >= 40) return 'bg-amber-500';
    return 'bg-cyan-500';
  };

  return (
    <div className="space-y-6">

      {/* Input Console */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 shadow-2xl space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-purple-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              AI-Powered Scam & Social Engineering Analyzer
            </h3>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400">Channel:</span>
            <select
              value={channel}
              onChange={(e) => setChannel(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-slate-950 border border-white/10 text-xs text-slate-200 focus:outline-none focus:border-purple-500 font-mono"
            >
              <option value="sms">SMS / Smishing</option>
              <option value="email">Email / Spear-phishing</option>
              <option value="whatsapp">WhatsApp / Telegram</option>
              <option value="job_offer">Recruitment Scam</option>
              <option value="crypto_alert">Crypto Investment Scam</option>
            </select>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            rows={5}
            value={messageText}
            onChange={(e) => setMessageText(e.target.value)}
            placeholder="Paste suspicious communication, email body, SMS text, or job recruitment pitch here..."
            className="w-full p-4 rounded-xl bg-slate-950/90 border border-white/10 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 font-mono transition-all resize-none"
          />

          <div className="flex items-center justify-between">
            <div className="text-xs text-slate-400 font-mono flex items-center space-x-2">
              <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
              <span>Evaluates Coercion Dimensions & Irreversible Payment IOCs</span>
            </div>

            <button
              type="submit"
              disabled={isLoading || !messageText.trim()}
              className="px-6 py-2.5 rounded-lg bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-400 hover:to-pink-500 text-white font-bold text-xs uppercase tracking-wider transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-lg shadow-purple-500/20"
            >
              {isLoading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Analyzing Linguistic Patterns...</span>
                </>
              ) : (
                <>
                  <span>Analyze Message</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Results Section */}
      {messageResult && !isLoading && (
        <div className="space-y-6">

          {/* Primary Result Banner */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 cyber-border">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-white/10">
              
              <div className="flex items-start space-x-4">
                <div className="p-4 rounded-2xl border border-purple-500/40 bg-purple-950/30 flex flex-col items-center justify-center min-w-[90px]">
                  <span className="text-2xl font-black font-mono text-purple-300">{messageResult.risk_score}</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider text-purple-400">Threat Score</span>
                </div>
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-extrabold uppercase border bg-purple-950/60 border-purple-500/40 text-purple-300">
                      {messageResult.risk_classification}
                    </span>
                    <span className="text-xs font-mono text-slate-400">
                      AI Confidence: {(messageResult.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mt-1">{messageResult.summary_verdict}</h3>
                  <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
                    {messageResult.executive_explanation}
                  </p>
                </div>
              </div>

            </div>

            {/* Extracted IOC Artifacts (Crypto Wallets, Phone numbers, URLs) */}
            <div className="mt-4 pt-4 border-t border-white/5 space-y-3">
              <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                Extracted Digital Forensic Artifacts (IOCs)
              </h5>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs font-mono">
                {/* Crypto Addresses */}
                <div className="p-3 rounded-xl bg-slate-950/70 border border-white/5 space-y-1">
                  <div className="flex items-center space-x-1.5 text-amber-400 text-[11px]">
                    <Wallet className="w-3.5 h-3.5" />
                    <span>Crypto Addresses ({messageResult.extracted_entities.crypto_addresses.length})</span>
                  </div>
                  {messageResult.extracted_entities.crypto_addresses.length > 0 ? (
                    messageResult.extracted_entities.crypto_addresses.map((w, idx) => (
                      <div key={idx} className="flex items-center justify-between text-slate-300">
                        <span className="truncate mr-1 text-[11px]">{w}</span>
                        <button onClick={() => copyToClipboard(w)} className="p-1 hover:text-white">
                          {copiedText === w ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3 text-slate-500" />}
                        </button>
                      </div>
                    ))
                  ) : (
                    <span className="text-slate-500 text-[11px]">None detected</span>
                  )}
                </div>

                {/* Extracted URLs */}
                <div className="p-3 rounded-xl bg-slate-950/70 border border-white/5 space-y-1">
                  <div className="flex items-center space-x-1.5 text-cyan-400 text-[11px]">
                    <LinkIcon className="w-3.5 h-3.5" />
                    <span>Embedded Links ({messageResult.extracted_entities.urls.length})</span>
                  </div>
                  {messageResult.extracted_entities.urls.length > 0 ? (
                    messageResult.extracted_entities.urls.map((u, idx) => (
                      <div key={idx} className="text-cyan-300 truncate text-[11px]">{u}</div>
                    ))
                  ) : (
                    <span className="text-slate-500 text-[11px]">None detected</span>
                  )}
                </div>

                {/* Impersonated Entities */}
                <div className="p-3 rounded-xl bg-slate-950/70 border border-white/5 space-y-1">
                  <div className="flex items-center space-x-1.5 text-rose-400 text-[11px]">
                    <Building2 className="w-3.5 h-3.5" />
                    <span>Targeted Entities</span>
                  </div>
                  {messageResult.extracted_entities.impersonated_entities.length > 0 ? (
                    <div className="text-rose-300 text-[11px] font-semibold">
                      {messageResult.extracted_entities.impersonated_entities.join(', ')}
                    </div>
                  ) : (
                    <span className="text-slate-500 text-[11px]">None identified</span>
                  )}
                </div>

                {/* Phone Numbers / UPI */}
                <div className="p-3 rounded-xl bg-slate-950/70 border border-white/5 space-y-1">
                  <div className="flex items-center space-x-1.5 text-emerald-400 text-[11px]">
                    <Phone className="w-3.5 h-3.5" />
                    <span>Contact Vectors</span>
                  </div>
                  <div className="text-slate-300 text-[11px] truncate">
                    {messageResult.extracted_entities.phone_numbers.length > 0
                      ? messageResult.extracted_entities.phone_numbers.join(', ')
                      : 'None detected'}
                  </div>
                </div>
              </div>
            </div>

            {/* Recommended Precautions */}
            {messageResult.recommended_actions.length > 0 && (
              <div className="mt-4 pt-4 border-t border-white/5">
                <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2">Immediate Safety Protocol</h5>
                <ul className="space-y-1 text-xs text-slate-300">
                  {messageResult.recommended_actions.map((act, idx) => (
                    <li key={idx} className="flex items-center space-x-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
                      <span>{act}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* 5-Factor Psychological Coercion Radar */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 space-y-4">
              <h4 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                <Cpu className="w-4 h-4 text-purple-400" />
                <span>Psychological Coercion Dimensions</span>
              </h4>

              <div className="space-y-3 font-mono text-xs">
                {Object.entries(messageResult.coercion_scores).map(([key, score]) => (
                  <div key={key} className="space-y-1">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="text-slate-300 capitalize">{key.replace(/_/g, ' ')}</span>
                      <span className="font-bold text-purple-300">{score}/100</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${getCoercionBarColor(score)}`}
                        style={{ width: `${score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Specific Social Engineering Indicators */}
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 space-y-4">
              <h4 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 text-rose-400" />
                <span>Social Engineering Indicators ({messageResult.indicators.length})</span>
              </h4>

              <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1">
                {messageResult.indicators.map((ind, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-950/70 border border-white/5 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-rose-300">{ind.title}</span>
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">
                        {ind.severity}
                      </span>
                    </div>
                    <div className="text-[11px] font-mono text-slate-300 bg-slate-900 px-2 py-1 rounded">
                      {ind.evidence}
                    </div>
                    <p className="text-[11px] text-slate-400">{ind.description}</p>
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* Web3 On-Chain Proof Card for Message Scam */}
          {messageResult.on_chain_proof && (
            <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900/90 via-purple-950/20 to-slate-900/90 border border-purple-500/40 space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                  Decentralized Scam Record (On-Chain Proof)
                </h4>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">
                  Privacy-Guaranteed
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Message content is kept 100% off-chain. The cryptographic commitment hash{' '}
                <code className="text-purple-300">{messageResult.on_chain_proof.report_hash}</code> has been anchored to prevent tampering.
              </p>
              <div className="flex justify-end">
                <button
                  onClick={() => onVerifyHash(messageResult.on_chain_proof!.report_hash)}
                  className="px-4 py-2 rounded-lg bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                >
                  <span>Verify On-Chain</span>
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

