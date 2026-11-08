export type RiskClassification = 
  | 'Low Risk' 
  | 'Suspicious' 
  | 'High Risk' 
  | 'Confirmed Malicious' 
  | 'Inconclusive';

export type IndicatorSeverity = 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface ThreatIndicator {
  category: string;
  severity: IndicatorSeverity;
  title: string;
  description: string;
  evidence: string;
  mitigation?: string;
}

export interface RedirectHop {
  hop_number: number;
  url: string;
  status_code: number;
  domain: string;
  ip_address?: string;
  is_cross_domain: boolean;
}

export interface SecurityHeaderFinding {
  header_name: string;
  status: 'PASS' | 'WARN' | 'FAIL';
  severity: IndicatorSeverity;
  value?: string;
  impact: string;
  remediation: string;
}

export interface CertificateDetails {
  subject_cn?: string;
  subject_alt_names: string[];
  issuer_org?: string;
  issuer_cn?: string;
  valid_from?: string;
  valid_to?: string;
  days_until_expiration?: number;
  signature_algorithm?: string;
  public_key_bits?: number;
  public_key_type?: string;
  is_expired: boolean;
  is_self_signed: boolean;
  is_hostname_mismatch: boolean;
  is_compromised_ca: boolean;
  ca_incident_notes?: string;
  raw_trust_chain: Array<{ subject: string; issuer: string }>;
  certificate_transparency_present: boolean;
}

export interface OnChainProof {
  report_hash: string;
  indicator_hash: string;
  risk_score: number;
  risk_class: RiskClassification;
  timestamp: number;
  reporter: string;
  tx_hash?: string;
  contract_address?: string;
  is_verified_on_chain: boolean;
  network: string;
}

export interface URLScanResult {
  scan_id: string;
  target_url: string;
  normalized_url: string;
  domain: string;
  ip_address?: string;
  timestamp: string;
  risk_score: number;
  risk_classification: RiskClassification;
  confidence: number;
  summary_verdict: string;
  executive_explanation: string;
  indicators: ThreatIndicator[];
  redirect_chain: RedirectHop[];
  certificate?: CertificateDetails;
  security_headers: SecurityHeaderFinding[];
  email_security?: Record<string, any>;
  recommended_precautions: string[];
  limitations: string;
  on_chain_proof?: OnChainProof;
}

export interface ExtractedEntities {
  urls: string[];
  domains: string[];
  emails: string[];
  phone_numbers: string[];
  crypto_addresses: string[];
  upi_handles: string[];
  impersonated_entities: string[];
}

export interface MessageScanResult {
  scan_id: string;
  timestamp: string;
  risk_score: number;
  risk_classification: RiskClassification;
  confidence: number;
  summary_verdict: string;
  executive_explanation: string;
  coercion_scores: Record<string, number>;
  extracted_entities: ExtractedEntities;
  indicators: ThreatIndicator[];
  recommended_actions: string[];
  limitations: string;
  on_chain_proof?: OnChainProof;
}

export interface GraphNode {
  id: string;
  label: string;
  node_type: 'DOMAIN' | 'IP' | 'CA' | 'PAYMENT' | 'CAMPAIGN' | 'MESSAGE';
  risk_level: string;
  details?: Record<string, any>;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: string;
}

export interface ThreatGraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  campaign_name?: string;
  correlated_incidents_count: number;
}

export interface DemoCase {
  id: string;
  type: 'URL' | 'MESSAGE';
  title: string;
  category: 'MALICIOUS' | 'BENIGN';
  input: string;
  description: string;
  expected_classification: string;
  highlights: string[];
}
