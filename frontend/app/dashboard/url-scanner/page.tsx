"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, Loader2, AlertTriangle, Shield, CheckCircle, ExternalLink } from "lucide-react";
import apiService from "@/services/api";
import { getRiskBadgeClass, formatDate } from "@/lib/utils";

export default function UrlScannerPage() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleScan = async () => {
    if (!url.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await apiService.analyzeUrl({ url: url.trim() });
      setResult(data);
    } catch (error: any) {
      console.error("Scan failed:", error);
      setResult({
        error: error.response?.data?.detail || "Analysis failed",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleScan();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">URL Threat Scanner</h1>
        <p className="text-gray-400">Analyze URLs for phishing, malware, and security threats</p>
      </div>

      {/* Scanner Input */}
      <Card className="glass-panel border-white/10">
        <CardHeader>
          <CardTitle>Enter URL to Analyze</CardTitle>
          <CardDescription>Paste a suspicious URL or domain to check for threats</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              type="text"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              className="flex-1 bg-white/5 border-white/10"
            />
            <Button
              onClick={handleScan}
              disabled={loading || !url.trim()}
              className="bg-cyber-blue hover:bg-cyber-blue/90"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Search className="mr-2 h-4 w-4" />
                  Scan URL
                </>
              )}
            </Button>
          </div>

          {/* Example URLs */}
          <div className="mt-4">
            <p className="text-xs text-gray-500 mb-2">Example URLs:</p>
            <div className="flex flex-wrap gap-2">
              {["https://google.com", "http://suspicious-site.xyz"].map((example) => (
                <button
                  key={example}
                  onClick={() => setUrl(example)}
                  className="text-xs px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white transition-colors"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <div className="space-y-6 animate-fade-in">
          {result.error ? (
            <Card className="glass-panel border-red-500/20">
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 text-red-400">
                  <AlertTriangle className="h-6 w-6" />
                  <div>
                    <p className="font-semibold">Analysis Failed</p>
                    <p className="text-sm">{result.error}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <>
              {/* Risk Overview */}
              <Card className="glass-panel border-white/10">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Risk Assessment</CardTitle>
                    <Badge className={getRiskBadgeClass(result.risk_level)}>
                      {result.risk_level}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="text-center p-4 rounded-lg bg-white/5">
                      <p className="text-sm text-gray-400 mb-1">Risk Score</p>
                      <p className="text-3xl font-bold text-cyber-blue">{result.risk_score || 0}</p>
                    </div>
                    <div className="text-center p-4 rounded-lg bg-white/5">
                      <p className="text-sm text-gray-400 mb-1">Confidence</p>
                      <p className="text-3xl font-bold text-cyber-cyan">
                        {((result.confidence || 0) * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="text-center p-4 rounded-lg bg-white/5">
                      <p className="text-sm text-gray-400 mb-1">Indicators</p>
                      <p className="text-3xl font-bold text-cyber-violet">
                        {result.indicators?.length || 0}
                      </p>
                    </div>
                  </div>

                  {result.result?.ai_summary && (
                    <div className="p-4 rounded-lg bg-cyber-blue/10 border border-cyber-blue/20">
                      <p className="text-sm leading-relaxed">{result.result.ai_summary}</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Domain Information */}
              {result.result?.domain_info && (
                <Card className="glass-panel border-white/10">
                  <CardHeader>
                    <CardTitle>Domain Information</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(result.result.domain_info).map(([key, value]: any) => (
                        <div key={key} className="flex justify-between items-center p-3 rounded bg-white/5">
                          <span className="text-sm text-gray-400 capitalize">
                            {key.replace(/_/g, " ")}:
                          </span>
                          <span className="text-sm font-mono">{value || "N/A"}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Threat Indicators */}
              {result.indicators && result.indicators.length > 0 && (
                <Card className="glass-panel border-white/10">
                  <CardHeader>
                    <CardTitle>Threat Indicators ({result.indicators.length})</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {result.indicators.map((indicator: any, index: number) => (
                        <div
                          key={index}
                          className="p-4 rounded-lg border border-white/10 bg-white/5"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              <AlertTriangle
                                className={`h-5 w-5 ${
                                  indicator.severity === "high" || indicator.severity === "critical"
                                    ? "text-red-500"
                                    : indicator.severity === "medium"
                                    ? "text-yellow-500"
                                    : "text-blue-500"
                                }`}
                              />
                              <span className="font-semibold">{indicator.type.replace(/_/g, " ")}</span>
                            </div>
                            <Badge variant="outline" className="text-xs">
                              {indicator.severity}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-400 mb-2">{indicator.description}</p>
                          {indicator.evidence && (
                            <p className="text-xs text-gray-500">Evidence: {indicator.evidence}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Recommendations */}
              {result.result?.recommendations && (
                <Card className="glass-panel border-white/10">
                  <CardHeader>
                    <CardTitle>Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.result.recommendations.map((rec: string, index: number) => (
                        <li key={index} className="flex items-start space-x-2">
                          <CheckCircle className="h-5 w-5 text-cyber-blue mt-0.5 flex-shrink-0" />
                          <span className="text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
