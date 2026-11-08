document.addEventListener('DOMContentLoaded', async () => {
  const urlInput = document.getElementById('urlInput');
  const scanBtn = document.getElementById('scanBtn');
  const resultDiv = document.getElementById('result');
  const riskBadge = document.getElementById('riskBadge');
  const verdict = document.getElementById('verdict');
  const explanation = document.getElementById('explanation');
  const proof = document.getElementById('proof');

  // Pre-fill active tab URL if available
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url && tab.url.startsWith('http')) {
      urlInput.value = tab.url;
    }
  } catch (e) {}

  scanBtn.addEventListener('click', async () => {
    const target = urlInput.value.trim();
    if (!target) return;

    scanBtn.textContent = 'Auditing Cryptographic Trust...';
    scanBtn.disabled = true;

    try {
      const response = await fetch('http://127.0.0.1:8000/api/analyze/url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: target, allow_redirects: true, record_on_chain: true })
      });

      const data = await response.json();
      resultDiv.style.display = 'block';

      const isMalicious = data.risk_score >= 55 || data.risk_classification.includes('Malicious') || data.risk_classification.includes('High');
      riskBadge.className = 'score-badge ' + (isMalicious ? 'critical' : 'safe');
      riskBadge.textContent = `${data.risk_classification.toUpperCase()} • SCORE ${data.risk_score}/100`;

      verdict.textContent = data.summary_verdict;
      explanation.textContent = data.executive_explanation;

      if (data.on_chain_proof) {
        proof.textContent = `On-Chain Proof: ${data.on_chain_proof.report_hash.slice(0, 16)}... (Keccak-256)`;
      }
    } catch (err) {
      resultDiv.style.display = 'block';
      verdict.textContent = 'Service Offline';
      explanation.textContent = 'Could not reach AegisTrust local backend (http://127.0.0.1:8000). Ensure the backend server is running.';
    } finally {
      scanBtn.textContent = 'Investigate Link';
      scanBtn.disabled = false;
    }
  });
});

