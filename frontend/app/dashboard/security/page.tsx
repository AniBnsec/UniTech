"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldCheck } from "lucide-react";

export default function SecurityPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Security Assessment</h1>
        <p className="text-gray-400">Website security header and configuration analysis</p>
      </div>
      <Card className="glass-panel border-white/10">
        <CardHeader><CardTitle><ShieldCheck className="inline h-5 w-5 mr-2" />Security Scanner</CardTitle></CardHeader>
        <CardContent><p className="text-gray-400">Security assessment tool coming soon...</p></CardContent>
      </Card>
    </div>
  );
}
