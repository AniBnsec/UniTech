"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Blocks, CheckCircle, XCircle, Loader2 } from "lucide-react";
import apiService from "@/services/api";

export default function BlockchainPage() {
  const [reportHash, setReportHash] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleVerify = async () => {
    if (!reportHash.trim() || reportHash.length !== 64) return;
    setLoading(true);
    setResult(null);

    try {
      const data = await apiService.verifyBlockchainRecord(reportHash.trim());
      setResult(data);
    } catch (error) {
      setResult({ valid: false, message: "Verification failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Blockchain Verification</h1>
        <p className="text-gray-400">Verify threat reports on blockchain</p>
      </div>

      <Card className="glass-panel border-white/10">
        <CardHeader>
          <CardTitle>Verify Report Hash</CardTitle>
          <CardDescription>Enter SHA-256 hash to verify on blockchain</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              type="text"
              placeholder="64-character SHA-256 hash"
              value={reportHash}
              onChange={(e) => setReportHash(e.target.value)}
              maxLength={64}
              className="flex-1 bg-white/5 border-white/10 font-mono text-sm"
            />
            <Button
              onClick={handleVerify}
              disabled={loading || reportHash.length !== 64}
              className="bg-cyber-blue hover:bg-cyber-blue/90"
            >
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Blocks className="mr-2 h-4 w-4" />}
              Verify
            </Button>
          </div>
        </CardContent>
      </Card>

      {result && (
        <Card className="glass-panel border-white/10 animate-fade-in">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Verification Result</CardTitle>
              <Badge variant={result.valid ? "default" : "destructive"}>
                {result.valid ? "Valid" : "Invalid"}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                {result.valid ? (
                  <CheckCircle className="h-6 w-6 text-green-500" />
                ) : (
                  <XCircle className="h-6 w-6 text-red-500" />
                )}
                <p className="text-sm">{result.message}</p>
              </div>

              {result.valid && result.transaction_hash && (
                <div className="p-4 rounded-lg bg-white/5 space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Transaction Hash:</span>
                    <span className="font-mono text-xs">{result.transaction_hash.slice(0, 20)}...</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Registered:</span>
                    <span>{result.registered_at ? new Date(result.registered_at).toLocaleDateString() : "N/A"}</span>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
