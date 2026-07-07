"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, ShieldCheck, Map, Scale, Users, FileText, Globe } from "lucide-react";
import Link from "next/link";

const features = [
  {
    icon: Map,
    title: "Scheme Discovery",
    desc: "Personalized AI recommendations based on your profile, income, and location.",
    href: "/dashboard",
  },
  {
    icon: Scale,
    title: "Policy Simplifier",
    desc: "Understand complex government circulars in plain language anyone can follow.",
    href: "/chat",
  },
  {
    icon: Users,
    title: "Civic Complaints",
    desc: "Upload a photo and AI generates the complaint for the right department.",
    href: "/chat",
  },
  {
    icon: FileText,
    title: "Document OCR",
    desc: "Verify Aadhaar, PAN, and other government IDs using AI-powered OCR.",
    href: "/dashboard",
  },
  {
    icon: Globe,
    title: "Multi-Language",
    desc: "Interact in Hindi or English — more regional languages coming soon.",
    href: "/chat",
  },
  {
    icon: ShieldCheck,
    title: "Secure & Private",
    desc: "JWT authentication, rate limiting, and encrypted data storage.",
    href: "/dashboard",
  },
];

export default function Home() {
  return (
    <section
      className="flex-1 flex flex-col items-center justify-center p-6 md:p-24 overflow-hidden relative"
      aria-labelledby="hero-heading"
    >
      <div className="z-10 w-full max-w-5xl flex flex-col items-center text-center space-y-8">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary backdrop-blur-sm"
          aria-label="Badge: India's First AI Civic Operating System"
        >
          <ShieldCheck className="mr-2 h-4 w-4" aria-hidden="true" />
          <span>India&apos;s First AI Civic Operating System</span>
        </motion.div>

        <motion.h1
          id="hero-heading"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl md:text-7xl font-extrabold tracking-tight"
        >
          One AI Companion for{" "}
          <br aria-hidden="true" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">
            Every Government Service.
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-lg md:text-xl text-muted-foreground max-w-2xl"
        >
          Discover schemes, file complaints, simplify policies, and automate paperwork
          with a simple conversation — in Hindi or English.
        </motion.p>

        <motion.nav
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-col sm:flex-row gap-4 w-full justify-center max-w-md"
          aria-label="Primary navigation actions"
        >
          <Link href="/chat" className="w-full sm:w-auto">
            <Button
              size="lg"
              className="w-full rounded-full shadow-lg shadow-blue-500/25 gap-2 group"
              aria-label="Start chatting with SmartBharat AI"
              id="cta-start-chat"
            >
              Start Chatting{" "}
              <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" aria-hidden="true" />
            </Button>
          </Link>
          <Link href="/dashboard" className="w-full sm:w-auto">
            <Button
              size="lg"
              variant="outline"
              className="w-full rounded-full backdrop-blur-md bg-background/50 gap-2"
              aria-label="Open citizen dashboard for scheme discovery"
              id="cta-dashboard"
            >
              <Map className="h-4 w-4" aria-hidden="true" />
              My Dashboard
            </Button>
          </Link>
        </motion.nav>
      </div>

      {/* Features Grid */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.5 }}
        className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-20 w-full max-w-5xl z-10"
        aria-label="SmartBharat AI features"
      >
        {features.map((feat, i) => (
          <Link
            key={feat.title}
            href={feat.href}
            className="p-6 rounded-2xl border bg-card/40 backdrop-blur-xl hover:bg-card/60 hover:border-primary/30 transition-all shadow-xl group focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background"
            aria-label={`${feat.title}: ${feat.desc}`}
          >
            <feat.icon
              className="h-10 w-10 text-primary mb-4 group-hover:scale-110 transition-transform"
              aria-hidden="true"
            />
            <h2 className="text-xl font-semibold mb-2">{feat.title}</h2>
            <p className="text-muted-foreground text-sm leading-relaxed">{feat.desc}</p>
          </Link>
        ))}
      </motion.section>

      {/* Stats bar */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.7, delay: 0.9 }}
        className="flex flex-wrap gap-8 justify-center mt-16 z-10"
        aria-label="SmartBharat AI statistics"
        role="region"
      >
        {[
          { value: "1000+", label: "Government Schemes" },
          { value: "28", label: "States Covered" },
          { value: "2", label: "Languages Supported" },
          { value: "99%", label: "AI Accuracy Score" },
        ].map(({ value, label }) => (
          <div key={label} className="text-center" aria-label={`${value} ${label}`}>
            <p className="text-3xl font-extrabold text-primary" aria-hidden="true">{value}</p>
            <p className="text-sm text-muted-foreground mt-1" aria-hidden="true">{label}</p>
          </div>
        ))}
      </motion.div>
    </section>
  );
}
