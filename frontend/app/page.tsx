"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Shield,
  Brain,
  Lock,
  Network,
  Zap,
  Globe,
  AlertTriangle,
  CheckCircle,
  ArrowRight,
  Search,
  FileText,
  Activity,
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-cyber-navy via-cyber-charcoal to-cyber-dark">
      {/* Navigation */}
      <nav className="border-b border-white/10 backdrop-blur-xl bg-cyber-navy/50 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Shield className="h-8 w-8 text-cyber-blue" />
              <span className="text-2xl font-bold text-gradient">ThreatShield</span>
            </div>
            <div className="hidden md:flex items-center space-x-6">
              <Link href="#features" className="text-gray-300 hover:text-white transition">
                Features
              </Link>
              <Link href="#how-it-works" className="text-gray-300 hover:text-white transition">
                How It Works
              </Link>
              <Link href="#about" className="text-gray-300 hover:text-white transition">
                About
              </Link>
              <Link href="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link href="/register">
                <Button className="bg-cyber-blue hover:bg-cyber-blue/90">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-cyber-blue/10 border border-cyber-blue/20 mb-6">
            <Zap className="h-4 w-4 text-cyber-blue" />
            <span className="text-sm text-cyber-blue font-medium">AI-Powered Threat Detection</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Protect Against
            <span className="text-gradient"> Digital Threats</span>
          </h1>
          
          <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
            Advanced cybersecurity intelligence platform combining AI, threat analysis, and blockchain 
            verification to detect phishing, scams, and security vulnerabilities in real-time.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <Link href="/register">
              <Button size="lg" className="bg-cyber-blue hover:bg-cyber-blue/90 text-white px-8">
                Start Free Analysis
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="#features">
              <Button size="lg" variant="outline" className="border-cyber-blue/30 hover:bg-cyber-blue/10">
                Learn More
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-cyber-blue mb-2">5+</div>
              <div className="text-sm text-gray-400">Analysis Engines</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-cyber-cyan mb-2">AI</div>
              <div className="text-sm text-gray-400">Powered Detection</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-cyber-violet mb-2">Web3</div>
              <div className="text-sm text-gray-400">Verified Reports</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Comprehensive Security Analysis</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Multiple layers of detection and analysis to identify threats before they cause harm
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glass-panel p-6 rounded-lg card-hover group"
            >
              <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-cyber-blue/20 to-cyber-violet/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <feature.icon className="h-6 w-6 text-cyber-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">How It Works</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Simple, fast, and comprehensive threat analysis in four steps
          </p>
        </div>

        <div className="grid md:grid-cols-4 gap-8 max-w-5xl mx-auto">
          {steps.map((step, index) => (
            <div key={index} className="text-center">
              <div className="h-16 w-16 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-violet flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
                {index + 1}
              </div>
              <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
              <p className="text-sm text-gray-400">{step.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="glass-panel p-12 rounded-2xl text-center max-w-3xl mx-auto">
          <Shield className="h-16 w-16 text-cyber-blue mx-auto mb-6" />
          <h2 className="text-3xl font-bold mb-4">Ready to Secure Your Digital Presence?</h2>
          <p className="text-gray-400 mb-8">
            Join security professionals and organizations using ThreatShield to detect and prevent cyber threats
          </p>
          <Link href="/register">
            <Button size="lg" className="bg-cyber-blue hover:bg-cyber-blue/90">
              Get Started Now - It's Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Shield className="h-6 w-6 text-cyber-blue" />
              <span className="font-semibold">ThreatShield</span>
            </div>
            <div className="text-sm text-gray-400">
              © 2024 ThreatShield. Built for cybersecurity education and research.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

const features = [
  {
    icon: Search,
    title: "URL Threat Analysis",
    description: "Detect phishing, typosquatting, and malicious domains with advanced AI-powered pattern recognition and threat intelligence.",
  },
  {
    icon: Lock,
    title: "TLS Certificate Validator",
    description: "Comprehensive certificate chain analysis, trust validation, and Certificate Transparency log verification.",
  },
  {
    icon: Brain,
    title: "AI Scam Detection",
    description: "Intelligent analysis of suspicious emails and messages to identify fraud, impersonation, and social engineering.",
  },
  {
    icon: Shield,
    title: "Security Assessment",
    description: "Non-intrusive website security checks including header analysis and configuration vulnerability detection.",
  },
  {
    icon: Network,
    title: "Threat Correlation",
    description: "Identify relationships between threats, track campaigns, and visualize attack infrastructure patterns.",
  },
  {
    icon: Globe,
    title: "Blockchain Verification",
    description: "Tamper-evident threat report registry on blockchain for transparent and independently verifiable intelligence.",
  },
];

const steps = [
  {
    title: "Submit",
    description: "Enter a URL, domain, or suspicious message for analysis",
  },
  {
    title: "Analyze",
    description: "AI and security engines perform comprehensive threat assessment",
  },
  {
    title: "Review",
    description: "Get detailed findings with evidence and risk classification",
  },
  {
    title: "Verify",
    description: "Optionally register findings on blockchain for verification",
  },
];
