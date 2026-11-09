"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { History as HistoryIcon, ChevronLeft, ChevronRight } from "lucide-react";
import apiService from "@/services/api";
import { formatDate, getRiskBadgeClass } from "@/lib/utils";

export default function HistoryPage() {
  const [investigations, setInvestigations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    loadInvestigations();
  }, [page]);

  const loadInvestigations = async () => {
    try {
      const data = await apiService.getInvestigations(page, 20);
      setInvestigations(data.items);
      setTotalPages(data.pages);
    } catch (error) {
      console.error("Failed to load history:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Investigation History</h1>
        <p className="text-gray-400">View all your past security analyses</p>
      </div>

      <Card className="glass-panel border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <HistoryIcon className="h-5 w-5" />
            <span>All Investigations</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8 text-gray-400">Loading...</div>
          ) : investigations.length > 0 ? (
            <>
              <div className="space-y-3">
                {investigations.map((inv) => (
                  <div
                    key={inv.id}
                    className="flex items-center justify-between p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
                  >
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-1">
                        <Badge variant="outline" className="text-xs">{inv.type}</Badge>
                        <span className="text-sm font-mono text-gray-400 truncate max-w-lg">
                          {inv.target}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500">{formatDate(inv.created_at)}</p>
                    </div>
                    <Badge className={getRiskBadgeClass(inv.risk_level || "UNKNOWN")}>
                      {inv.risk_level || "Pending"}
                    </Badge>
                  </div>
                ))}
              </div>

              <div className="flex items-center justify-between mt-6">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                >
                  <ChevronLeft className="h-4 w-4 mr-1" />
                  Previous
                </Button>
                <span className="text-sm text-gray-400">
                  Page {page} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage(page + 1)}
                  disabled={page === totalPages}
                >
                  Next
                  <ChevronRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
            </>
          ) : (
            <div className="text-center py-8 text-gray-400">
              <p>No investigations yet</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
