import React, { useState, useEffect, useMemo } from 'react';
import { ThreatGraphData, GraphNode } from '../types';
import { 
  Network, Server, Globe, Lock, Wallet, Flag, ShieldAlert, 
  Info, RefreshCw, ZoomIn, ZoomOut, RotateCcw, Filter
} from 'lucide-react';

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
  const [filterType, setFilterType] = useState<string>('ALL');
  const [zoomLevel, setZoomLevel] = useState<number>(1);

  useEffect(() => {
    if (graphData && graphData.nodes.length > 0 && !selectedNode) {
      setSelectedNode(graphData.nodes[0]);
    }
  }, [graphData]);

  // Compute 2D node coordinates in a visual hub-and-spoke layout
  const nodePositions = useMemo(() => {
    if (!graphData || graphData.nodes.length === 0) return {};
    const positions: Record<string, { x: number; y: number }> = {};
    const centerX = 360;
    const centerY = 240;

    // Find central campaign node if exists
    const campaignNode = graphData.nodes.find(n => n.node_type === 'CAMPAIGN');
    if (campaignNode) {
      positions[campaignNode.id] = { x: centerX, y: centerY };
    }

    const otherNodes = graphData.nodes.filter(n => n.node_type !== 'CAMPAIGN');
    const total = otherNodes.length;
    const radius = 170;

    otherNodes.forEach((node, idx) => {
      const angle = (idx / total) * 2 * Math.PI - Math.PI / 2;
      positions[node.id] = {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      };
    });

    return positions;
  }, [graphData]);

  const getNodeColor = (type: string, risk: string) => {
    if (type === 'CAMPAIGN') return '#ff0055'; // neon rose
    if (type === 'IP') return '#ff7a00';       // orange
    if (type === 'DOMAIN') return '#00f0ff';   // cyan
    if (type === 'CA') return '#ffb700';       // amber
    if (type === 'PAYMENT') return '#9d4edd';  // purple
    return '#64748b';
  };

  const filteredNodes = useMemo(() => {
    if (!graphData) return [];
    if (filterType === 'ALL') return graphData.nodes;
    return graphData.nodes.filter(n => n.node_type === filterType);
  }, [graphData, filterType]);

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
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-950/90 border border-white/10 min-h-[520px] relative flex flex-col justify-between overflow-hidden">
          
          {/* Controls Bar */}
          <div className="flex flex-wrap items-center justify-between gap-2 z-20 pb-3 border-b border-white/5">
            <div className="flex items-center space-x-1.5 text-xs font-mono">
              <Filter className="w-3.5 h-3.5 text-slate-400" />
              <button
                onClick={() => setFilterType('ALL')}
                className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                  filterType === 'ALL' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400 hover:text-white'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setFilterType('DOMAIN')}
                className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                  filterType === 'DOMAIN' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400 hover:text-white'
                }`}
              >
                Domains
              </button>
              <button
                onClick={() => setFilterType('IP')}
                className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                  filterType === 'IP' ? 'bg-orange-500/20 text-orange-300 border border-orange-500/40' : 'text-slate-400 hover:text-white'
                }`}
              >
                IPs
              </button>
              <button
                onClick={() => setFilterType('CA')}
                className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                  filterType === 'CA' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'text-slate-400 hover:text-white'
                }`}
              >
                CAs
              </button>
              <button
                onClick={() => setFilterType('PAYMENT')}
                className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                  filterType === 'PAYMENT' ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40' : 'text-slate-400 hover:text-white'
                }`}
              >
                Wallets
              </button>
            </div>

            <div className="flex items-center space-x-1">
              <button
                onClick={() => setZoomLevel(prev => Math.min(prev + 0.15, 1.6))}
                className="p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-300"
                title="Zoom In"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setZoomLevel(prev => Math.max(prev - 0.15, 0.7))}
                className="p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-300"
                title="Zoom Out"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setZoomLevel(1)}
                className="p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-300"
                title="Reset View"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* SVG Canvas */}
          <div className="relative flex-1 flex items-center justify-center overflow-hidden my-2">
            <svg
              viewBox="0 0 720 480"
              className="w-full h-full max-h-[460px] transition-transform duration-300 ease-out select-none"
              style={{ transform: `scale(${zoomLevel})` }}
            >
              <defs>
                <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#ff0055" stopOpacity="0.6" />
                </linearGradient>
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
              </defs>

              {/* Concentric Radar Rings */}
              <circle cx="360" cy="240" r="80" fill="none" stroke="rgba(255,255,255,0.04)" strokeDasharray="4 4" />
              <circle cx="360" cy="240" r="170" fill="none" stroke="rgba(255,255,255,0.06)" strokeDasharray="6 6" />

              {/* Edges / Lines between nodes */}
              {graphData?.edges.map((edge, idx) => {
                const src = nodePositions[edge.source];
                const dst = nodePositions[edge.target];
                if (!src || !dst) return null;

                const midX = (src.x + dst.x) / 2;
                const midY = (src.y + dst.y) / 2;

                return (
                  <g key={idx}>
                    <line
                      x1={src.x}
                      y1={src.y}
                      x2={dst.x}
                      y2={dst.y}
                      stroke="url(#edgeGrad)"
                      strokeWidth="1.8"
                      strokeOpacity="0.5"
                    />
                    {/* Animated Pulse along the edge */}
                    <circle r="2.5" fill="#00f0ff">
                      <animateMotion
                        path={`M ${src.x} ${src.y} L ${dst.x} ${dst.y}`}
                        dur={`${2.5 + (idx % 3)}s`}
                        repeatCount="indefinite"
                      />
                    </circle>
                    {/* Edge Label */}
                    <text
                      x={midX}
                      y={midY - 4}
                      fill="#94a3b8"
                      fontSize="9"
                      fontFamily="monospace"
                      textAnchor="middle"
                    >
                      {edge.relation}
                    </text>
                  </g>
                );
              })}

              {/* Render Nodes */}
              {filteredNodes.map((node) => {
                const pos = nodePositions[node.id] || { x: 360, y: 240 };
                const isSelected = selectedNode?.id === node.id;
                const color = getNodeColor(node.node_type, node.risk_level);

                return (
                  <g
                    key={node.id}
                    className="cursor-pointer transition-all"
                    onClick={() => setSelectedNode(node)}
                  >
                    {/* Pulsing Selection Outer Ring */}
                    {isSelected && (
                      <circle
                        cx={pos.x}
                        cy={pos.y}
                        r="28"
                        fill="none"
                        stroke={color}
                        strokeWidth="2"
                        opacity="0.8"
                        filter="url(#glow)"
                      />
                    )}

                    {/* Node Core Circle */}
                    <circle
                      cx={pos.x}
                      cy={pos.y}
                      r={node.node_type === 'CAMPAIGN' ? '22' : '16'}
                      fill="#070b14"
                      stroke={color}
                      strokeWidth={isSelected ? '3' : '2'}
                      filter="url(#glow)"
                    />

                    {/* Center Dot */}
                    <circle
                      cx={pos.x}
                      cy={pos.y}
                      r="4"
                      fill={color}
                    />

                    {/* Label */}
                    <text
                      x={pos.x}
                      y={pos.y + (node.node_type === 'CAMPAIGN' ? 34 : 26)}
                      fill="#f1f5f9"
                      fontSize="10"
                      fontWeight="bold"
                      fontFamily="monospace"
                      textAnchor="middle"
                      className="pointer-events-none select-none"
                    >
                      {node.label.length > 22 ? node.label.slice(0, 20) + '...' : node.label}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>

          <div className="text-[11px] text-slate-500 font-mono flex items-center justify-between border-t border-white/5 pt-2">
            <span className="flex items-center space-x-1.5">
              <Info className="w-3.5 h-3.5 text-cyan-400" />
              <span>Click any node in the SVG topology to inspect attribution forensics.</span>
            </span>
            <span>{graphData?.nodes.length || 0} Entities Correlated</span>
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
                <strong>Campaign Correlation:</strong> Individual phishing lures often appear isolated to victims, but backend graph correlation links shared hosting ASNs, common TLS issuers, and unified money-mule payment vectors.
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
