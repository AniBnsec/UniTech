import React from 'react';
import { DemoCase } from '../types';
import { AlertTriangle, CheckCircle2, Zap, ArrowRight } from 'lucide-react';

interface DemoBarProps {
  demoCases: DemoCase[];
  onSelectCase: (demo: DemoCase) => void;
  isLoading: boolean;
}

export const DemoBar: React.FC<DemoBarProps> = ({ demoCases, onSelectCase, isLoading }) => {
  if (!demoCases || demoCases.length === 0) return null;

  const maliciousCases = demoCases.filter(c => c.category === 'MALICIOUS');
  const benignCases = demoCases.filter(c => c.category === 'BENIGN');

  return (
    <div className="mb-8 p-4 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950/80 border border-white/10 cyber-border">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <Zap className="w-4 h-4 text-cyan-400 animate-pulse" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Hackathon Live Evaluation Suite (6 Test Cases)
          </h3>
        </div>
        <span className="text-[11px] text-slate-400">
          Click any scenario to auto-populate and run instant investigation
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Malicious Scenarios Column */}
        <div className="space-y-2">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-rose-400 px-1">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Malicious Scenarios (Typosquatting / eMudhra CA / SMS Scam)</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {maliciousCases.map((demo) => (
              <button
                key={demo.id}
                disabled={isLoading}
                onClick={() => onSelectCase(demo)}
                className="text-left p-2.5 rounded-xl bg-rose-950/20 hover:bg-rose-900/30 border border-rose-800/30 hover:border-rose-500/50 transition-all group disabled:opacity-50"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-rose-900/60 text-rose-300 border border-rose-700/40 font-bold">
                    {demo.type}
                  </span>
                  <ArrowRight className="w-3 h-3 text-rose-400/60 group-hover:text-rose-300 group-hover:translate-x-0.5 transition-transform" />
                </div>
                <div className="text-xs font-semibold text-rose-100 line-clamp-1 group-hover:text-white">
                  {demo.title}
                </div>
                <div className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                  {demo.description}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Benign Scenarios Column */}
        <div className="space-y-2">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-emerald-400 px-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Benign Ground Truth (Legitimate Bank / Enterprise / University)</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {benignCases.map((demo) => (
              <button
                key={demo.id}
                disabled={isLoading}
                onClick={() => onSelectCase(demo)}
                className="text-left p-2.5 rounded-xl bg-emerald-950/20 hover:bg-emerald-900/30 border border-emerald-800/30 hover:border-emerald-500/50 transition-all group disabled:opacity-50"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-emerald-900/60 text-emerald-300 border border-emerald-700/40 font-bold">
                    {demo.type}
                  </span>
                  <ArrowRight className="w-3 h-3 text-emerald-400/60 group-hover:text-emerald-300 group-hover:translate-x-0.5 transition-transform" />
                </div>
                <div className="text-xs font-semibold text-emerald-100 line-clamp-1 group-hover:text-white">
                  {demo.title}
                </div>
                <div className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                  {demo.description}
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

