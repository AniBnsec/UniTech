import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "OPERATIONAL"

    res_h = client.get("/health")
    assert res_h.status_code == 200
    assert res_h.json()["status"] == "healthy"

def test_demo_cases_endpoint():
    res = client.get("/api/demo/cases")
    assert res.status_code == 200
    cases = res.json()
    assert len(cases) == 6
    # 3 malicious, 3 benign
    assert sum(1 for c in cases if c["category"] == "MALICIOUS") == 3
    assert sum(1 for c in cases if c["category"] == "BENIGN") == 3

def test_analyze_url_endpoint():
    payload = {
        "url": "https://paypaI-security-update.com/login",
        "allow_redirects": False,
        "record_on_chain": True
    }
    res = client.post("/api/analyze/url", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["domain"] == "paypai-security-update.com"
    assert data["risk_classification"] in ["High Risk", "Confirmed Malicious"]
    assert data["on_chain_proof"] is not None
    assert data["on_chain_proof"]["report_hash"].startswith("0x")

def test_analyze_message_endpoint():
    payload = {
        "message_text": "URGENT: Legal notice from Cyber Crime Division. Your bank account is frozen. Click https://sbi-kyc-panupdate.top or deposit to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa immediately.",
        "channel_type": "sms",
        "record_on_chain": True
    }
    res = client.post("/api/analyze/message", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["risk_score"] >= 70
    assert len(data["extracted_entities"]["crypto_addresses"]) > 0
    assert data["on_chain_proof"] is not None

def test_threat_graph_endpoint():
    res = client.get("/api/threats/graph")
    assert res.status_code == 200
    graph = res.json()
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) > 0

def test_blockchain_status_and_verify():
    status_res = client.get("/api/blockchain/status")
    assert status_res.status_code == 200
    assert "zero_pii_policy" in status_res.json()

    # Submit a scan and verify its hash
    url_res = client.post("/api/analyze/url", json={"url": "https://test-verify.com", "allow_redirects": False})
    report_hash = url_res.json()["on_chain_proof"]["report_hash"]

    verify_res = client.get(f"/api/blockchain/verify/{report_hash}")
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "VALID_AND_TAMPER_PROOF"
    assert verify_res.json()["details"]["report_hash"] == report_hash
