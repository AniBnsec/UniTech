import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { DemoBar } from './components/DemoBar';
import { UrlScannerTab } from './components/UrlScannerTab';
import { MessageScannerTab } from './components/MessageScannerTab';
import { ThreatGraphTab } from './components/ThreatGraphTab';
import { VerifyPortalTab } from './components/VerifyPortalTab';
import { URLScanResult, MessageScanResult, ThreatGraphData, DemoCase } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'url' | 'message' | 'graph' | 'verify'>('url');
  
  // State for scanners
  const [targetUrl, setTargetUrl] = useState('');
  const [urlResult, setUrlResult] = useState<URLScanResult | null>(null);
  const [isUrlLoading, setIsUrlLoading] = useState(false);

  const [messageText, setMessageText] = useState('');
  const [messageResult, setMessageResult] = useState<MessageScanResult | null>(null);
  const [isMessageLoading, setIsMessageLoading] = useState(false);

  const [graphData, setGraphData] = useState<ThreatGraphData | null>(null);
  const [isGraphLoading, setIsGraphLoading] = useState(false);

  const [verifyHashToOpen, setVerifyHashToOpen] = useState('');
  const [demoCases, setDemoCases] = useState<DemoCase[]>([]);

  const [systemStatus, setSystemStatus] = useState({
    online: true,
    network: 'EVM Local / Sepolia',
    contractAddress: '0x5FbDB2315678afecb367f032d93F642f64180aa3'
  });

  // Fetch initial demos and threat graph
  useEffect(() => {
    fetch('/api/demo/cases')
      .then(r => r.json())
      .then(data => setDemoCases(data))
      .catch(() => {});

    fetch('/api/threats/graph')
      .then(r => r.json())
      .then(data => setGraphData(data))
      .catch(() => {});

    fetch('/api/blockchain/status')
      .then(r => r.json())
      .then(data => {
        setSystemStatus(prev => ({
          ...prev,
          network: data.network || 'EVM Local / Sepolia',
          contractAddress: data.contract_address || prev.contractAddress
        }));
      })
      .catch(() => {});
  }, []);

  // Handlers for URL Scan
  const handleScanUrl = async (url: string, allowRedirects: boolean, recordOnChain: boolean) => {
    setIsUrlLoading(true);
    try {
      const res = await fetch('/api/analyze/url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url,
          allow_redirects: allowRedirects,
          record_on_chain: recordOnChain
        })
      });
      const data = await res.json();
      setUrlResult(data);
      // Refresh graph to reflect any new correlated indicators
      fetch('/api/threats/graph').then(r => r.json()).then(g => setGraphData(g)).catch(() => {});
    } catch (err) {
      console.error(err);
    } finally {
      setIsUrlLoading(false);
    }
  };

  // Handlers for Message Scan
  const handleScanMessage = async (text: string, channel: string) => {
    setIsMessageLoading(true);
    try {
      const res = await fetch('/api/analyze/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_text: text,
          channel_type: channel,
          record_on_chain: true
        })
      });
      const data = await res.json();
      setMessageResult(data);
      fetch('/api/threats/graph').then(r => r.json()).then(g => setGraphData(g)).catch(() => {});
    } catch (err) {
      console.error(err);
    } finally {
      setIsMessageLoading(false);
    }
  };

  // Handler for 1-click Demo Case Selection
  const handleSelectDemo = (demo: DemoCase) => {
    if (demo.type === 'URL') {
      setActiveTab('url');
      setTargetUrl(demo.input);
      handleScanUrl(demo.input, true, true);
    } else {
      setActiveTab('message');
      setMessageText(demo.input);
      handleScanMessage(demo.input, 'sms');
    }
  };

  // Handler for jumping to Verify Portal with hash
  const handleVerifyHash = (hash: string) => {
    setVerifyHashToOpen(hash);
    setActiveTab('verify');
  };

  const handleRefreshGraph = () => {
    setIsGraphLoading(true);
    fetch('/api/threats/graph')
      .then(r => r.json())
      .then(data => setGraphData(data))
      .finally(() => setIsGraphLoading(false));
  };

  return (
    <div className="min-h-screen bg-[#070b14] flex flex-col justify-between">
      <div>
        <Navbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          systemStatus={systemStatus}
        />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          
          {/* Quick-Load Demo Suite */}
          <DemoBar
            demoCases={demoCases}
            onSelectCase={handleSelectDemo}
            isLoading={isUrlLoading || isMessageLoading}
          />

          {/* Active Tab Router */}
          {activeTab === 'url' && (
            <UrlScannerTab
              onScan={handleScanUrl}
              scanResult={urlResult}
              isLoading={isUrlLoading}
              onVerifyHash={handleVerifyHash}
              targetUrl={targetUrl}
              setTargetUrl={setTargetUrl}
            />
          )}

          {activeTab === 'message' && (
            <MessageScannerTab
              onScanMessage={handleScanMessage}
              messageResult={messageResult}
              isLoading={isMessageLoading}
              messageText={messageText}
              setMessageText={setMessageText}
              onVerifyHash={handleVerifyHash}
            />
          )}

          {activeTab === 'graph' && (
            <ThreatGraphTab
              graphData={graphData}
              onRefreshGraph={handleRefreshGraph}
              isLoading={isGraphLoading}
            />
          )}

          {activeTab === 'verify' && (
            <VerifyPortalTab
              key={verifyHashToOpen}
              initialHash={verifyHashToOpen}
            />
          )}

        </main>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/5 py-6 text-center text-xs text-slate-500 font-mono">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AegisTrust Platform • AI Cybersecurity & Web3 Trust Intelligence</span>
          <span>Zero-PII On-Chain Guarantee • EVM Keccak-256 Provenance</span>
        </div>
      </footer>
    </div>
  );
};

export default App;

