import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  AuthResponse,
  LoginCredentials,
  RegisterData,
  UrlAnalysisRequest,
  UrlAnalysisResult,
  TlsAnalysisResult,
  MessageAnalysisRequest,
  MessageAnalysisResult,
  SecurityAssessmentResult,
  Investigation,
  DashboardStats,
  ThreatGraph,
  BlockchainRecord,
  VerificationResult,
  User,
  ApiResponse,
  PaginatedResponse,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.clearToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );

    // Load token from localStorage if available
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  getToken(): string | null {
    return this.token;
  }

  // Authentication Endpoints
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/register', data);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/login', credentials);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async logout(): Promise<void> {
    this.clearToken();
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/api/auth/me');
    return response.data;
  }

  // URL Analysis Endpoints
  async analyzeUrl(data: UrlAnalysisRequest): Promise<UrlAnalysisResult> {
    const response = await this.client.post<UrlAnalysisResult>('/api/analyze/url', data);
    return response.data;
  }

  async analyzeDomain(domain: string): Promise<UrlAnalysisResult> {
    const response = await this.client.post<UrlAnalysisResult>('/api/analyze/domain', { domain });
    return response.data;
  }

  // TLS Certificate Analysis
  async analyzeTls(hostname: string): Promise<TlsAnalysisResult> {
    const response = await this.client.post<TlsAnalysisResult>('/api/analyze/tls', { hostname });
    return response.data;
  }

  // Message Analysis
  async analyzeMessage(data: MessageAnalysisRequest): Promise<MessageAnalysisResult> {
    const response = await this.client.post<MessageAnalysisResult>('/api/analyze/message', data);
    return response.data;
  }

  // Security Assessment
  async assessSecurity(url: string): Promise<SecurityAssessmentResult> {
    const response = await this.client.post<SecurityAssessmentResult>('/api/analyze/security', { url });
    return response.data;
  }

  // Investigations
  async getInvestigations(page: number = 1, pageSize: number = 20): Promise<PaginatedResponse<Investigation>> {
    const response = await this.client.get<PaginatedResponse<Investigation>>('/api/investigations', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  async getInvestigation(id: string): Promise<Investigation> {
    const response = await this.client.get<Investigation>(`/api/investigations/${id}`);
    return response.data;
  }

  // Dashboard Statistics
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await this.client.get<DashboardStats>('/api/dashboard/stats');
    return response.data;
  }

  // Threat Intelligence
  async getThreatGraph(filters?: any): Promise<ThreatGraph> {
    const response = await this.client.get<ThreatGraph>('/api/threats/graph', { params: filters });
    return response.data;
  }

  async getThreatRelationships(entityId: string): Promise<any> {
    const response = await this.client.get(`/api/threats/${entityId}/relationships`);
    return response.data;
  }

  // Blockchain Endpoints
  async registerOnBlockchain(investigationId: string): Promise<BlockchainRecord> {
    const response = await this.client.post<BlockchainRecord>('/api/blockchain/register', {
      investigation_id: investigationId,
    });
    return response.data;
  }

  async verifyBlockchainRecord(reportHash: string): Promise<VerificationResult> {
    const response = await this.client.post<VerificationResult>('/api/blockchain/verify', {
      report_hash: reportHash,
    });
    return response.data;
  }

  async getBlockchainRecords(page: number = 1): Promise<PaginatedResponse<BlockchainRecord>> {
    const response = await this.client.get<PaginatedResponse<BlockchainRecord>>('/api/blockchain/records', {
      params: { page },
    });
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService;
