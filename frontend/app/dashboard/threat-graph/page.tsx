"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Network } from "lucide-react";

export default function ThreatGraphPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Threat Correlation Graph</h1>
        <p className="text-gray-400">Visualize relationships between threats</p>
      </div>
      <Card className="glass-panel border-white/10">
        <CardHeader><CardTitle><Network className="inline h-5 w-5 mr-2" />Threat Relationships</CardTitle></CardHeader>
        <CardContent><p className="text-gray-400">Threat correlation visualization coming soon...</p></CardContent>
      </Card>
    </div>
  );
}
