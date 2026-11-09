import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ThreatShield - AI-Powered Threat Detection Platform",
  description: "Advanced cybersecurity intelligence platform combining AI, threat analysis, and blockchain verification",
  keywords: ["cybersecurity", "threat intelligence", "phishing detection", "AI security", "blockchain verification"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
