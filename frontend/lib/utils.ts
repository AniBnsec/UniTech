import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d);
}

export function getRiskColor(risk: string): string {
  const riskLower = risk.toLowerCase();
  
  if (riskLower.includes('low')) return 'text-risk-low';
  if (riskLower.includes('suspicious')) return 'text-risk-suspicious';
  if (riskLower.includes('high') || riskLower.includes('critical')) return 'text-risk-high';
  if (riskLower.includes('malicious')) return 'text-risk-critical';
  
  return 'text-muted-foreground';
}

export function getRiskBadgeClass(risk: string): string {
  const riskLower = risk.toLowerCase();
  
  if (riskLower.includes('low')) return 'bg-risk-low/20 text-risk-low border-risk-low/30';
  if (riskLower.includes('suspicious')) return 'bg-risk-suspicious/20 text-risk-suspicious border-risk-suspicious/30';
  if (riskLower.includes('high') || riskLower.includes('critical')) return 'bg-risk-high/20 text-risk-high border-risk-high/30';
  if (riskLower.includes('malicious')) return 'bg-risk-critical/20 text-risk-critical border-risk-critical/30';
  
  return 'bg-muted/20 text-muted-foreground border-muted/30';
}

export function truncateUrl(url: string, maxLength: number = 50): string {
  if (url.length <= maxLength) return url;
  
  const start = url.substring(0, maxLength / 2);
  const end = url.substring(url.length - maxLength / 2);
  
  return `${start}...${end}`;
}

export function formatRiskScore(score: number): string {
  return score.toFixed(0);
}
