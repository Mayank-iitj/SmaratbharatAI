"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, Bell, CheckCircle2, AlertCircle } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="flex-1 p-6 md:p-12 max-w-7xl mx-auto w-full z-10 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Citizen Dashboard</h1>
          <p className="text-muted-foreground mt-1">Welcome back, Rahul. Here is your civic overview.</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium">Civic Health Score</p>
            <p className="text-2xl font-bold text-primary">850/1000</p>
          </div>
          <div className="h-16 w-16 rounded-full border-4 border-primary/20 bg-primary/10 flex items-center justify-center relative">
            <svg viewBox="0 0 36 36" className="absolute inset-0 w-full h-full text-primary -rotate-90">
              <path
                className="stroke-current opacity-20"
                strokeWidth="3"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className="stroke-current"
                strokeWidth="3"
                strokeDasharray="85, 100"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <span className="text-lg font-bold">850</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Recommended Schemes */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><CheckCircle2 className="h-5 w-5 text-green-500" /> Recommended Schemes</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-3 rounded-lg border bg-background/50 hover:bg-muted/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-sm">PM Kisan Samman Nidhi</h3>
                <p className="text-xs text-muted-foreground mt-1">92% Match based on your profile.</p>
              </div>
              <div className="p-3 rounded-lg border bg-background/50 hover:bg-muted/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-sm">Stand-Up India</h3>
                <p className="text-xs text-muted-foreground mt-1">85% Match for your new business.</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Complaints Tracker */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }}>
          <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><AlertCircle className="h-5 w-5 text-orange-500" /> Active Complaints</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">Pothole on Main Road</span>
                  <span className="text-blue-500 text-xs px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20">In Progress</span>
                </div>
                <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 w-[60%]" />
                </div>
                <p className="text-xs text-muted-foreground text-right">Est. Resolution: 2 Days</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Document Vault */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.2 }}>
          <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><FileText className="h-5 w-5 text-purple-500" /> Smart Vault</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-lg border bg-background/50">
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">PDF</div>
                  <div>
                    <p className="text-sm font-medium">Aadhaar Card</p>
                    <p className="text-[10px] text-muted-foreground">Verified</p>
                  </div>
                </div>
                <CheckCircle2 className="h-4 w-4 text-green-500" />
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg border border-orange-500/30 bg-orange-500/5">
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded bg-orange-500/10 flex items-center justify-center text-orange-500 font-bold text-xs">JPG</div>
                  <div>
                    <p className="text-sm font-medium">Driving License</p>
                    <p className="text-[10px] text-orange-500">Expires in 14 days</p>
                  </div>
                </div>
                <AlertCircle className="h-4 w-4 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

    </div>
  );
}
