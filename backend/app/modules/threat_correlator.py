from typing import Dict, List, Optional
import collections
from app.schemas.threat import (
    GraphNode,
    GraphEdge,
    ThreatGraphData,
    URLScanResult,
    MessageScanResult
)

class ThreatCorrelator:
    """
    In-memory correlation and clustering graph engine linking submitted indicators across incidents.
    """
    def __init__(self):
        # Index records:
        # domain -> [scan_ids]
        self.domain_index: Dict[str, List[str]] = collections.defaultdict(list)
        # ip -> [domains]
        self.ip_to_domains: Dict[str, List[str]] = collections.defaultdict(list)
        # ca_org -> [domains]
        self.ca_to_domains: Dict[str, List[str]] = collections.defaultdict(list)
        # payment/wallet -> [scan_ids]
        self.payment_to_scans: Dict[str, List[str]] = collections.defaultdict(list)
        # scan_history: scan_id -> dict
        self.scans: Dict[str, dict] = {}

    def register_url_scan(self, result: URLScanResult):
        """Indexes a completed URL scan to detect multi-site campaigns."""
        self.scans[result.scan_id] = {
            "type": "URL",
            "domain": result.domain,
            "ip": result.ip_address,
            "risk_score": result.risk_score,
            "risk_class": result.risk_classification.value,
            "ca_org": result.certificate.issuer_org if result.certificate else None
        }

        self.domain_index[result.domain].append(result.scan_id)

        if result.ip_address:
            if result.domain not in self.ip_to_domains[result.ip_address]:
                self.ip_to_domains[result.ip_address].append(result.domain)

        if result.certificate and result.certificate.issuer_org:
            if result.domain not in self.ca_to_domains[result.certificate.issuer_org]:
                self.ca_to_domains[result.certificate.issuer_org].append(result.domain)

    def register_message_scan(self, result: MessageScanResult):
        """Indexes a completed message scan."""
        self.scans[result.scan_id] = {
            "type": "MESSAGE",
            "risk_score": result.risk_score,
            "risk_class": result.risk_classification.value,
            "wallets": result.extracted_entities.crypto_addresses,
            "urls": result.extracted_entities.urls
        }
        for wallet in result.extracted_entities.crypto_addresses:
            self.payment_to_scans[wallet].append(result.scan_id)

    def generate_correlation_graph(self, focus_domain: Optional[str] = None) -> ThreatGraphData:
        """
        Builds a node-edge graph topology representing connected digital threat infrastructure.
        """
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        added_node_ids = set()

        def add_node(node: GraphNode):
            if node.id not in added_node_ids:
                nodes.append(node)
                added_node_ids.add(node.id)

        # Baseline seed nodes if registry is fresh
        if not self.ip_to_domains and not self.ca_to_domains:
            # Generate realistic multi-target campaign cluster (e.g. Banking Phishing Campaign)
            campaign_id = "camp-hydra-sbi"
            add_node(GraphNode(
                id=campaign_id,
                label="Campaign: FinPhish-Cluster-India",
                node_type="CAMPAIGN",
                risk_level="CRITICAL",
                details={"target_sector": "Banking & Financial Services", "actor_profile": "Organized Cyber Syndicate"}
            ))

            shared_ip = "185.220.101.45"
            add_node(GraphNode(
                id=shared_ip,
                label=f"Bulletproof Hosting IP: {shared_ip}",
                node_type="IP",
                risk_level="HIGH",
                details={"asn": "AS49870", "country": "RU"}
            ))
            edges.append(GraphEdge(source=campaign_id, target=shared_ip, relation="OPERATES_ON"))

            mock_domains = [
                ("onlinesbi.sbi-login.xyz", "CRITICAL"),
                ("sbi-kyc-panupdate.top", "CRITICAL"),
                ("onlinesbi.secure-banking.net", "HIGH")
            ]
            for dom, risk in mock_domains:
                add_node(GraphNode(id=dom, label=dom, node_type="DOMAIN", risk_level=risk))
                edges.append(GraphEdge(source=dom, target=shared_ip, relation="RESOLVES_TO"))
                edges.append(GraphEdge(source=dom, target=campaign_id, relation="PART_OF_CAMPAIGN"))

            ca_name = "eMudhra Compromised Sub-CA"
            add_node(GraphNode(id=ca_name, label=ca_name, node_type="CA", risk_level="CRITICAL"))
            edges.append(GraphEdge(source="onlinesbi.sbi-login.xyz", target=ca_name, relation="SIGNED_BY"))

            wallet_addr = "0x71C...4982"
            add_node(GraphNode(id=wallet_addr, label=f"Mule Wallet: {wallet_addr}", node_type="PAYMENT", risk_level="CRITICAL"))
            edges.append(GraphEdge(source=campaign_id, target=wallet_addr, relation="REUSES_PAYMENT"))

            return ThreatGraphData(
                nodes=nodes,
                edges=edges,
                campaign_name="FinPhish-Cluster-India (Correlated Infrastructure)",
                correlated_incidents_count=4
            )

        # Dynamic graph generation from registered scans
        for ip, domains in self.ip_to_domains.items():
            ip_node_id = f"ip-{ip}"
            add_node(GraphNode(id=ip_node_id, label=f"IP: {ip}", node_type="IP", risk_level="HIGH"))
            for dom in domains:
                dom_node_id = f"dom-{dom}"
                add_node(GraphNode(id=dom_node_id, label=dom, node_type="DOMAIN", risk_level="HIGH"))
                edges.append(GraphEdge(source=dom_node_id, target=ip_node_id, relation="RESOLVES_TO"))

        for ca_org, domains in self.ca_to_domains.items():
            ca_node_id = f"ca-{ca_org[:20]}"
            is_compromised = "emudhra" in ca_org.lower() or "diginotar" in ca_org.lower()
            add_node(GraphNode(id=ca_node_id, label=f"CA: {ca_org}", node_type="CA", risk_level="CRITICAL" if is_compromised else "INFO"))
            for dom in domains:
                dom_node_id = f"dom-{dom}"
                edges.append(GraphEdge(source=dom_node_id, target=ca_node_id, relation="SIGNED_BY"))

        for wallet, scans in self.payment_to_scans.items():
            w_id = f"wallet-{wallet[:10]}"
            add_node(GraphNode(id=w_id, label=f"Wallet: {wallet[:10]}...", node_type="PAYMENT", risk_level="CRITICAL"))
            for s in scans:
                edges.append(GraphEdge(source=s, target=w_id, relation="REUSES_PAYMENT"))

        return ThreatGraphData(
            nodes=nodes,
            edges=edges,
            campaign_name="Correlated Incident Graph",
            correlated_incidents_count=len(self.scans)
        )

# Global singleton
correlator = ThreatCorrelator()

