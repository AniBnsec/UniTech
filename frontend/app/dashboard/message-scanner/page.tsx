"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MessageSquare, Loader2, AlertTriangle, CheckCircle } from "lucide-react";
import apiService from "@/services/api";
import { getRiskBadgeClass } from "@/lib/utils";

export default function MessageScannerPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleScan = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await apiService.analyzeMessage({
        message_text: message.trim(),
        message_type: "other",
      });
      setResult(data);
    } catch (error: any) {
      console.error("Scan failed:", error);
      setResult({ error: error.response?.data?.detail || "Analysis failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Message Scam Scanner</h1>
        <p className="text-gray-400">Detect phishing and fraud in emails, SMS, and messages</p>
      </div>

      <Card className="glass-panel border-white/10">
        <CardHeader>
          <CardTitle>Paste Suspicious Message</CardTitle>
          <CardDescription>Analyze emails, SMS, or WhatsApp messages for scam indicators</CardDescription>
        </CardHeader>
        <CardContent>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={loading}
            placeholder="Paste the complete message text here..."
            className="w-full min-h-[200px] p-4 rounded-lg bg-white/5 border border-white/10 focus:border-cyber-blue focus:ring-1 focus:ring-cyber-blue resize-none"
          />
          <Button
            onClick={handleScan}
            disabled={loading || !message.trim()}
            className="mt-4 bg-cyber-blue hover:bg-cyber-blue/90"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <MessageSquare className="mr-2 h-4 w-4" />
                Analyze Message
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && !result.error && (
        <div className="space-y-6 animate-fade-in">
          <Card className="glass-panel border-white/10">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Analysis Result</CardTitle>
                <Badge className={getRiskBadgeClass(result.risk_level)}>
                  {result.risk_level}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {result.result?.ai_analysis && (
                  <div className="p-4 rounded-lg bg-cyber-blue/10 border border-cyber-blue/20">
                    <p className="text-sm leading-relaxed">{result.result.ai_analysis}</p>
                  </div>
                )}

                {result.result?.suspicious_patterns && result.result.suspicious_patterns.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-2">Suspicious Patterns Detected:</h3>
                    <ul className="space-y-1">
                      {result.result.suspicious_patterns.map((pattern: string, i: number) => (
                        <li key={i} className="flex items-center space-x-2 text-sm">
                          <AlertTriangle className="h-4 w-4 text-yellow-500" />
                          <span>{pattern}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {result.result?.recommendations && (
                  <div>
                    <h3 className="font-semibold mb-2">Recommendations:</h3>
                    <ul className="space-y-1">
                      {result.result.recommendations.map((rec: string, i: number) => (
                        <li key={i} className="flex items-start space-x-2 text-sm">
                          <CheckCircle className="h-4 w-4 text-cyber-blue mt-0.5 flex-shrink-0" />
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
