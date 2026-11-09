"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Globe, Loader2 } from "lucide-react";
import apiService from "@/services/api";

export default function DomainIntelPage() {
  const [domain, setDomain] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!domain.trim()) return;
    setLoading(true);
    try {
      await apiService.analyzeDomain(domain.trim());
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Domain Intelligence</h1>
        <p className="text-gray-400">Comprehensive domain analysis and reputation check</p>
      </div>
      <Card className="glass-panel border-white/10">
        <CardHeader><CardTitle>Analyze Domain</CardTitle></CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              placeholder="example.com"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              className="flex-1 bg-white/5 border-white/10"
            />
            <Button onClick={handleAnalyze} disabled={loading}>
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Globe className="mr-2 h-4 w-4" />}
              Analyze
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
