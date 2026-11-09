"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Shield,
  AlertTriangle,
  CheckCircle,
  Activity,
  TrendingUp,
  Clock,
} from "lucide-react";
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import apiService from "@/services/api";
import { formatDate, getRiskBadgeClass } from "@/lib/utils";
import Link from "next/link";

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await apiService.getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error("Failed to load stats:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse-glow text-cyber-blue">
          <Shield className="h-12 w-12" />
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: "Total Scans",
      value: stats?.total_investigations || 0,
      icon: Shield,
      color: "text-cyber-blue",
      bgColor: "bg-cyber-blue/10",
    },
    {
      title: "Low Risk",
      value: stats?.low_risk_count || 0,
      icon: CheckCircle,
      color: "text-green-500",
      bgColor: "bg-green-500/10",
    },
    {
      title: "Suspicious",
      value: stats?.suspicious_count || 0,
      icon: AlertTriangle,
      color: "text-yellow-500",
      bgColor: "bg-yellow-500/10",
    },
    {
      title: "High Risk",
      value: (stats?.high_risk_count || 0) + (stats?.malicious_count || 0),
      icon: AlertTriangle,
      color: "text-red-500",
      bgColor: "bg-red-500/10",
    },
  ];

  const threatData = stats?.threat_categories || [];
  const activityData = stats?.daily_activity || [];

  const COLORS = ["#3B82F6", "#06B6D4", "#8B5CF6", "#F59E0B"];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Security Dashboard</h1>
        <p className="text-gray-400">Monitor threats and analyze security posture</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <Card key={index} className="glass-panel border-white/10">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">{stat.title}</p>
                  <p className="text-3xl font-bold">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <Card className="glass-panel border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5 text-cyber-blue" />
              <span>Activity Trend</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                <XAxis dataKey="date" stroke="#888" fontSize={12} />
                <YAxis stroke="#888" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1a1f2e",
                    border: "1px solid #ffffff20",
                    borderRadius: "8px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="count"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  dot={{ fill: "#3B82F6" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Threat Categories */}
        <Card className="glass-panel border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-cyber-blue" />
              <span>Threat Distribution</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={threatData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {threatData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1a1f2e",
                    border: "1px solid #ffffff20",
                    borderRadius: "8px",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Investigations */}
      <Card className="glass-panel border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Clock className="h-5 w-5 text-cyber-blue" />
              <span>Recent Investigations</span>
            </div>
            <Link href="/dashboard/history" className="text-sm text-cyber-blue hover:underline">
              View All
            </Link>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {stats?.recent_investigations && stats.recent_investigations.length > 0 ? (
            <div className="space-y-3">
              {stats.recent_investigations.map((investigation: any) => (
                <div
                  key={investigation.id}
                  className="flex items-center justify-between p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-1">
                      <Badge variant="outline" className="text-xs">
                        {investigation.type}
                      </Badge>
                      <span className="text-sm font-mono text-gray-400 truncate max-w-md">
                        {investigation.target}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">{formatDate(investigation.created_at)}</p>
                  </div>
                  <Badge className={getRiskBadgeClass(investigation.risk_level || "UNKNOWN")}>
                    {investigation.risk_level || "Pending"}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">
              <Shield className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No investigations yet</p>
              <p className="text-sm">Start scanning URLs or messages to see results here</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
