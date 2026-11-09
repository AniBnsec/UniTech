"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Lock, Loader2, Shield, CheckCircle, XCircle } from "lucide-react";
import apiService from "@/services/api";
import { getRiskBadgeClass } from "@/lib/utils";

export default function TlsAnalyzerPage() {
  const [hostname, setHostname] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!hostname.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const data = await apiService.analyzeTls(hostname.trim());
      setResult(data);
    } catch (error) {
      setResult({ error: "Analysis failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">TLS Certificate Analyzer</h1>
        <p className="text-gray-400">Validate SSL/TLS certificates and trust</p>
      </div>

      <Card className="glass-panel border-white/10">
        <CardHeader>
          <CardTitle>Enter Hostname</CardTitle>
          <CardDescription>Check TLS certificate validity and configuration</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              type="text"
              placeholder="example.com"
              value={hostname}
              onChange={(e) => setHostname(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleAnalyze()}
              disabled={loading}
              className="flex-1 bg-white/5 border-white/10"
            />
            <Button
              onClick={handleAnalyze}
              disabled={loading || !hostname.trim()}
              className="bg-cyber-blue hover:bg-cyber-blue/90"
            >
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Lock className="mr-2 h-4 w-4" />}
              Analyze
            </Button>
          </div>
        </CardContent>
      </Card>

      {result && !result.error && (
        <Card className="glass-panel border-white/10 animate-fade-in">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Certificate Analysis</CardTitle>
              <Badge className={getRiskBadgeClass(result.risk_level)}>
                {result.risk_level}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {result.result?.certificate && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-3 rounded bg-white/5">
                    <p className="text-xs text-gray-400 mb-1">Subject</p>
                    <p className="text-sm font-mono">{result.result.certificate.subject}</p>
                  </div>
                  <div className="p-3 rounded bg-white/5">
                    <p className="text-xs text-gray-400 mb-1">Issuer</p>
                    <p className="text-sm font-mono">{result.result.certificate.issuer}</p>
                  </div>
                  <div className="p-3 rounded bg-white/5">
                    <p className="text-xs text-gray-400 mb-1">Valid Until</p>
                    <p className="text-sm">{new Date(result.result.certificate.valid_until).toLocaleDateString()}</p>
                  </div>
                  <div className="p-3 rounded bg-white/5">
                    <p className="text-xs text-gray-400 mb-1">Days Until Expiry</p>
                    <p className="text-sm">{result.result.days_until_expiry || 0} days</p>
                  </div>
                </div>
              )}

              {result.result?.warnings && result.result.warnings.length > 0 && (
                <div>
                  <h3 className="font-semibold mb-2">Warnings:</h3>
                  <ul className="space-y-2">
                    {result.result.warnings.map((warning: string, i: number) => (
                      <li key={i} className="flex items-center space-x-2 text-sm">
                        <XCircle className="h-4 w-4 text-yellow-500" />
                        <span>{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
