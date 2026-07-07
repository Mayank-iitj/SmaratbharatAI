"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Mic, ShieldCheck, Map, Users, Scale } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center p-6 md:p-24 overflow-hidden relative">
      
      <div className="z-10 w-full max-w-5xl flex flex-col items-center text-center space-y-8">
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary backdrop-blur-sm"
        >
          <ShieldCheck className="mr-2 h-4 w-4" />
          <span>India's First AI Civic Operating System</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl md:text-7xl font-extrabold tracking-tight"
        >
          One AI Companion for <br />
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
          Discover schemes, file complaints, simplify policies, and automate paperwork with a simple conversation.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-col sm:flex-row gap-4 w-full justify-center max-w-md"
        >
          <Link href="/chat" className="w-full sm:w-auto">
            <Button size="lg" className="w-full rounded-full shadow-lg shadow-blue-500/25 gap-2 group">
              Start Chatting <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
          <Link href="/dashboard" className="w-full sm:w-auto">
            <Button size="lg" variant="outline" className="w-full rounded-full backdrop-blur-md bg-background/50 gap-2">
              <Mic className="h-4 w-4" /> Try Voice Search
            </Button>
          </Link>
        </motion.div>
      </div>

      {/* Features Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.5 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-24 w-full max-w-5xl z-10"
      >
        {[
          { icon: Map, title: "Scheme Discovery", desc: "Personalized AI recommendations based on your profile." },
          { icon: Scale, title: "Policy Simplifier", desc: "Understand complex government circulars in simple language." },
          { icon: Users, title: "Civic Complaints", desc: "Just upload a photo, and AI generates the complaint for the right department." }
        ].map((feat, i) => (
          <div key={i} className="p-6 rounded-2xl border bg-card/40 backdrop-blur-xl hover:bg-card/60 transition-colors shadow-xl">
            <feat.icon className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">{feat.title}</h3>
            <p className="text-muted-foreground">{feat.desc}</p>
          </div>
        ))}
      </motion.div>

    </main>
  );
}
