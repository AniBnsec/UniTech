// User and Authentication Types
export interface User {
  id: string;
  email: string;
  username: string;
  role: 'user' | 'analyst' | 'admin';
  created_at: string;
  verified: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

// Risk and Threat Types
export type RiskLevel = 'LOW_RISK' | 'SUSPICIOUS' | 'HIGH_RISK' | 'CRITICAL' | 'MALICIOUS' | 'INCONCLUSIVE';

export interface ThreatIndicator {
  id: string;
  type: string;
  value: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  evidence: string;
  source: string;
}

export interface IntelligenceMatch {
  id: string;
  source: string;
  matched_value: string;
  threat_type: string;
  confidence: number;
  first_seen?: string;
  last_seen?: string;
  tags?: string[];
}

// URL Analysis Types
export interface UrlAnalysisRequest {
  url: string;
  deep_scan?: boolean;
}

export interface DomainInfo {
  domain: string;
  subdomain?: string;
  tld: string;
  registered_domain: string;
  ip_address?: string;
  nameservers?: string[];
  creation_date?: string;
  expiration_date?: string;
  registrar?: string;
}

export interface RedirectInfo {
  original_url: string;
  final_url: string;
  redirect_chain: string[];
  redirect_count: number;
  suspicious: boolean;
  reason?: string;
}

export interface UrlAnalysisResult {
  id: string;
  url: string;
  normalized_url: string;
  risk_level: RiskLevel;
  risk_score: number;
  confidence: number;
  domain_info: DomainInfo;
  indicators: ThreatIndicator[];
  intelligence_matches: IntelligenceMatch[];
  redirect_info?: RedirectInfo;
  ai_summary: string;
  recommendations: string[];
  analyzed_at: string;
  analysis_coverage: {
    url_structure: boolean;
    domain_reputation: boolean;
    threat_intelligence: boolean;
    redirect_analysis: boolean;
    dns_check: boolean;
  };
}

// TLS Certificate Types
export interface Certificate {
  subject: string;
  issuer: string;
  valid_from: string;
  valid_until: string;
  serial_number: string;
  signature_algorithm: string;
  public_key_algorithm: string;
  key_size: number;
  subject_alt_names: string[];
  fingerprint_sha256: string;
}

export interface CertificateChain {
  leaf_certificate: Certificate;
  intermediate_certificates: Certificate[];
  root_certificate?: Certificate;
  chain_valid: boolean;
  trust_status: string;
}

export interface TlsAnalysisResult {
  id: string;
  hostname: string;
  https_available: boolean;
  certificate?: Certificate;
  certificate_chain?: CertificateChain;
  hostname_match: boolean;
  expired: boolean;
  days_until_expiry?: number;
  tls_version: string;
  cipher_suite?: string;
  certificate_transparency: boolean;
  revocation_checked: boolean;
  revoked: boolean;
  warnings: string[];
  risk_level: RiskLevel;
  analyzed_at: string;
}

// Message Analysis Types
export interface MessageAnalysisRequest {
  message_text: string;
  message_type?: 'email' | 'sms' | 'whatsapp' | 'other';
  sender?: string;
}

export interface ExtractedIndicator {
  type: 'url' | 'email' | 'phone' | 'payment' | 'credential_request';
  value: string;
  suspicious: boolean;
  reason?: string;
}

export interface MessageAnalysisResult {
  id: string;
  message_type: string;
  risk_level: RiskLevel;
  risk_score: number;
  suspicious_patterns: string[];
  extracted_indicators: ExtractedIndicator[];
  impersonation_detected: boolean;
  impersonated_entity?: string;
  urgency_manipulation: boolean;
  ai_analysis: string;
  recommendations: string[];
  analyzed_at: string;
}

// Security Assessment Types
export interface SecurityHeader {
  name: string;
  value?: string;
  present: boolean;
  severity: 'info' | 'low' | 'medium' | 'high';
  description: string;
  recommendation?: string;
}

export interface SecurityFinding {
  id: string;
  title: string;
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  description: string;
  evidence: string;
  impact: string;
  remediation: string;
  category: string;
}

export interface SecurityAssessmentResult {
  id: string;
  url: string;
  https_enabled: boolean;
  headers: SecurityHeader[];
  findings: SecurityFinding[];
  tls_configuration: string;
  mixed_content: boolean;
  overall_score: number;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  analyzed_at: string;
}

// Threat Correlation Types
export interface ThreatRelationship {
  source_id: string;
  target_id: string;
  relationship_type: string;
  confidence: number;
  evidence: string;
  discovered_at: string;
}

export interface ThreatEntity {
  id: string;
  type: 'url' | 'domain' | 'message' | 'certificate' | 'indicator';
  value: string;
  risk_level: RiskLevel;
  first_seen: string;
  last_seen: string;
  occurrence_count: number;
}

export interface ThreatGraph {
  entities: ThreatEntity[];
  relationships: ThreatRelationship[];
}

// Blockchain Types
export interface BlockchainRecord {
  id: string;
  report_id: string;
  report_hash: string;
  transaction_hash: string;
  block_number: number;
  chain_id: number;
  submitter_address: string;
  registered_at: string;
  verified: boolean;
}

export interface VerificationResult {
  valid: boolean;
  on_chain: boolean;
  hash_match: boolean;
  registered_at?: string;
  transaction_hash?: string;
  message: string;
}

// Investigation Types
export interface Investigation {
  id: string;
  user_id: string;
  type: 'url' | 'domain' | 'message' | 'tls' | 'security';
  target: string;
  risk_level: RiskLevel;
  risk_score: number;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  result?: any;
  created_at: string;
  completed_at?: string;
}

// Dashboard Statistics
export interface DashboardStats {
  total_investigations: number;
  low_risk_count: number;
  suspicious_count: number;
  high_risk_count: number;
  malicious_count: number;
  recent_investigations: Investigation[];
  threat_categories: {
    category: string;
    count: number;
  }[];
  daily_activity: {
    date: string;
    count: number;
  }[];
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
