import React, { useState, useEffect } from 'react';
import { ThreatGraphData, GraphNode } from '../types';
import { Network, Server, Globe, Lock, Wallet, Flag, ShieldAlert, Info, RefreshCw } from 'lucide-react';

interface ThreatGraphTabProps {
  graphData: ThreatGraphData | null;
  onRefreshGraph: () => void;
  isLoading: boolean;
}

export const ThreatGraphTab: React.FC<ThreatGraphTabProps> = ({
  graphData,
  onRefreshGraph,
  isLoading
}) => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);

  useEffect(() => {
    if (graphData && graphData.nodes.length > 0 && !selectedNode) {
      setSelectedNode(graphData.nodes[0]);
    }
  }, [graphData]);

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'CAMPAIGN': return <Flag className="w-4 h-4 text-rose-400" />;
      case 'IP': return <Server className="w-4 h-4 text-orange-400" />;
      case 'DOMAIN': return <Globe className="w-4 h-4 text-cyan-400" />;
      case 'CA': return <Lock className="w-4 h-4 text-amber-400" />;
      case 'PAYMENT': return <Wallet className="w-4 h-4 text-purple-400" />;
      default: return <ShieldAlert className="w-4 h-4 text-slate-400" />;
    }
  };

  const getNodeBorder = (risk: string) => {
    switch (risk) {
      case 'CRITICAL': return 'border-rose-500/80 bg-rose-950/40 text-rose-200';
      case 'HIGH': return 'border-orange-500/80 bg-orange-950/40 text-orange-200';
      case 'MEDIUM': return 'border-amber-500/80 bg-amber-950/40 text-amber-200';
      default: return 'border-cyan-500/60 bg-cyan-950/30 text-cyan-200';
    }
  };

  return (
    <div className="space-y-6">

      {/* Header Info Banner */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Network className="w-5 h-5 text-emerald-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              Intelligent Threat Infrastructure Correlation Graph
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Correlates individual submissions across shared DNS hosts, bulletproof IP subnets, compromised CAs, and reused cryptocurrency wallets.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <span className="text-xs font-mono text-emerald-400 bg-emerald-950/50 px-3 py-1.5 rounded-lg border border-emerald-800/40">
            Campaign: {graphData?.campaign_name || 'Active Threat Intelligence Cluster'}
          </span>
          <button
            onClick={onRefreshGraph}
            disabled={isLoading}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
            title="Refresh Graph"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Main Interactive Graph Canvas & Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Visual Topology Canvas */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-950/90 border border-white/10 min-h-[460px] relative flex flex-col justify-between overflow-hidden">
          
          {/* Subtle Grid Background Pattern */}
          <div className="absolute inset-0 opacity-15 pointer-events-none" style={{
            backgroundImage: 'radial-gradient(circle, #00f0ff 1px, transparent 1px)',
            backgroundSize: '24px 24px'
          }} />

          {/* Node Grid Layout */}
          <div className="relative z-10 space-y-6">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 border-b border-white/5 pb-2">
              <span>Topological Nodes ({graphData?.nodes.length || 0})</span>
              <span>Edges: Shared Infrastructure & Certificates</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              {graphData?.nodes.map((node) => {
                const isSelected = selectedNode?.id === node.id;
                return (
                  <div
                    key={node.id}
                    onClick={() => setSelectedNode(node)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer ${getNodeBorder(node.risk_level)} ${
                      isSelected ? 'ring-2 ring-cyan-400 scale-[1.02] shadow-xl' : 'hover:scale-[1.01]'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center space-x-1.5">
                        {getNodeIcon(node.node_type)}
                        <span className="text-[10px] font-mono uppercase font-bold tracking-wider">
                          {node.node_type}
                        </span>
                      </div>
                      <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-black/40 border border-white/10">
                        {node.risk_level}
                      </span>
                    </div>
                    <div className="text-xs font-bold text-white truncate">
                      {node.label}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Edge Connections List */}
            <div className="pt-4 border-t border-white/5">
              <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2">Correlated Attack Vectors</h5>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
                {graphData?.edges.map((edge, idx) => (
                  <div key={idx} className="p-2 rounded bg-slate-900/60 border border-white/5 flex items-center justify-between text-[11px]">
                    <span className="text-cyan-300 truncate max-w-[110px]">{edge.source}</span>
                    <span className="text-[9px] uppercase px-1.5 py-0.5 bg-black/50 text-slate-400 rounded">
                      {edge.relation}
                    </span>
                    <span className="text-purple-300 truncate max-w-[110px]">{edge.target}</span>
                  </div>
                ))}
              </div>
            </div>

          </div>

          <div className="relative z-10 text-[11px] text-slate-500 font-mono mt-4 flex items-center space-x-2">
            <Info className="w-3.5 h-3.5" />
            <span>Click any entity card to inspect threat intelligence telemetry and attribution clues.</span>
          </div>
        </div>

        {/* Selected Node Forensics Sidebar */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-white/10 space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-white/10">
            <ShieldAlert className="w-4 h-4 text-cyan-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Entity Forensics Inspector
            </h4>
          </div>

          {selectedNode ? (
            <div className="space-y-4 text-xs font-mono">
              <div className="space-y-1">
                <span className="text-[10px] text-slate-500 block uppercase">Identifier</span>
                <span className="text-sm font-bold text-white break-all">{selectedNode.label}</span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="p-2.5 rounded-lg bg-slate-950 border border-white/5">
                  <span className="text-slate-500 block">Node Type</span>
                  <span className="text-cyan-300 font-bold">{selectedNode.node_type}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-950 border border-white/5">
                  <span className="text-slate-500 block">Risk Status</span>
                  <span className="text-rose-400 font-bold">{selectedNode.risk_level}</span>
                </div>
              </div>

              {selectedNode.details && (
                <div className="space-y-2">
                  <span className="text-[10px] text-slate-500 block uppercase">Metadata & Attribution Clues</span>
                  <div className="p-3 rounded-xl bg-slate-950 border border-white/5 space-y-1.5 text-[11px]">
                    {Object.entries(selectedNode.details).map(([k, v]) => (
                      <div key={k} className="flex justify-between">
                        <span className="text-slate-400 capitalize">{k.replace(/_/g, ' ')}:</span>
                        <span className="text-slate-200 font-semibold">{String(v)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="p-3 rounded-xl bg-cyan-950/20 border border-cyan-800/30 text-[11px] text-cyan-300 leading-relaxed font-sans">
                <strong>Campaign Correlation:</strong> Individual phishing lures often appear isolated to victims, but backend analysis reveals shared hosting ASNs, common TLS issuers, and unified money-mule payment vectors.
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-xs text-slate-500">
              Select an entity node to inspect its telemetry.
            </div>
          )}
        </div>

      </div>

    </div>
  );
};

