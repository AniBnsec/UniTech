"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Shield,
  LayoutDashboard,
  Search,
  Globe,
  MessageSquare,
  Lock,
  ShieldCheck,
  Network,
  Blocks,
  History,
  User,
  LogOut,
  Menu,
  X,
} from "lucide-react";
import apiService from "@/services/api";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = apiService.getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    // Fetch user data
    apiService.getCurrentUser().then(setUser).catch(() => {
      router.push("/login");
    });
  }, [router]);

  const handleLogout = () => {
    apiService.logout();
    router.push("/");
  };

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "URL Scanner", href: "/dashboard/url-scanner", icon: Search },
    { name: "Domain Intel", href: "/dashboard/domain-intel", icon: Globe },
    { name: "Message Scanner", href: "/dashboard/message-scanner", icon: MessageSquare },
    { name: "TLS Analyzer", href: "/dashboard/tls-analyzer", icon: Lock },
    { name: "Security Assessment", href: "/dashboard/security", icon: ShieldCheck },
    { name: "Threat Graph", href: "/dashboard/threat-graph", icon: Network },
    { name: "Blockchain", href: "/dashboard/blockchain", icon: Blocks },
    { name: "History", href: "/dashboard/history", icon: History },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-cyber-navy via-cyber-charcoal to-cyber-dark">
      {/* Top Navigation */}
      <nav className="border-b border-white/10 backdrop-blur-xl bg-cyber-navy/50 sticky top-0 z-50">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden"
              >
                {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </Button>
              <Link href="/dashboard" className="flex items-center space-x-2">
                <Shield className="h-7 w-7 text-cyber-blue" />
                <span className="text-xl font-bold text-gradient">ThreatShield</span>
              </Link>
            </div>

            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-2 text-sm text-gray-400">
                <User className="h-4 w-4" />
                <span>{user?.username || "User"}</span>
              </div>
              <Button variant="ghost" size="icon" onClick={handleLogout}>
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`${
            sidebarOpen ? "translate-x-0" : "-translate-x-full"
          } fixed md:sticky top-[57px] left-0 z-40 h-[calc(100vh-57px)] w-64 border-r border-white/10 bg-cyber-navy/50 backdrop-blur-xl transition-transform md:translate-x-0`}
        >
          <nav className="space-y-1 p-4">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? "bg-cyber-blue/20 text-cyber-blue border border-cyber-blue/30"
                      : "text-gray-400 hover:bg-white/5 hover:text-white"
                  }`}
                >
                  <item.icon className="h-5 w-5" />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 md:p-8">
          <div className="max-w-7xl mx-auto">{children}</div>
        </main>
      </div>
    </div>
  );
}
