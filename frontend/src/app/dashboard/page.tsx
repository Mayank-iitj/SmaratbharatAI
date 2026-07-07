"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, CheckCircle2, AlertCircle, User, Search, Upload } from "lucide-react";

interface SchemeRecommendation {
  content: string;
  score: number;
}

interface CitizenProfile {
  state: string;
  occupation: string;
  income: string;
  gender: string;
  category: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function DashboardPage() {
  const [profile, setProfile] = useState<CitizenProfile>({
    state: "",
    occupation: "",
    income: "",
    gender: "",
    category: "",
  });
  const [recommendations, setRecommendations] = useState<SchemeRecommendation[]>([]);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingRecs(true);
    const query = `${profile.occupation} in ${profile.state} with income ${profile.income}, category: ${profile.category}, gender: ${profile.gender}`;
    try {
      const res = await fetch(
        `${API_URL}/api/schemes/recommendations?user_id=user_123&query=${encodeURIComponent(query)}`
      );
      const data = await res.json();
      setRecommendations(data.recommendations || []);
    } catch {
      setRecommendations([]);
    } finally {
      setLoadingRecs(false);
    }
  };

  const handleDocumentUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploadStatus("Analyzing document…");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${API_URL}/api/documents/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setUploadStatus(
        data.status === "success"
          ? `✅ Verified: ${data.extracted_data?.document_type || "Document"}`
          : "❌ Could not verify document."
      );
    } catch {
      setUploadStatus("❌ Upload failed. Please try again.");
    }
  };

  return (
    <section
      className="flex-1 p-6 md:p-12 max-w-7xl mx-auto w-full z-10 space-y-8"
      aria-labelledby="dashboard-heading"
    >
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 id="dashboard-heading" className="text-3xl font-bold tracking-tight">
            Citizen Dashboard
          </h1>
          <p className="text-muted-foreground mt-1">
            Discover your eligible schemes, track complaints, and manage documents.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block" aria-label="Civic Health Score: 850 out of 1000">
            <p className="text-sm font-medium">Civic Health Score</p>
            <p className="text-2xl font-bold text-primary" aria-hidden="true">850/1000</p>
          </div>
          <div
            className="h-16 w-16 rounded-full border-4 border-primary/20 bg-primary/10 flex items-center justify-center relative"
            role="img"
            aria-label="Civic health score: 85%"
          >
            <svg viewBox="0 0 36 36" className="absolute inset-0 w-full h-full text-primary -rotate-90" aria-hidden="true">
              <path className="stroke-current opacity-20" strokeWidth="3" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path className="stroke-current" strokeWidth="3" strokeDasharray="85, 100" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <span className="text-lg font-bold" aria-hidden="true">850</span>
          </div>
        </div>
      </div>

      {/* Profile-based scheme discovery */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5 text-primary" aria-hidden="true" />
              Personalized Scheme Discovery
            </CardTitle>
            <CardDescription>
              Fill in your profile to get AI-powered scheme recommendations tailored for you.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form
              onSubmit={handleProfileSubmit}
              aria-label="Citizen profile form for personalized scheme recommendations"
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
            >
              {/* State */}
              <div className="flex flex-col gap-1">
                <label htmlFor="state" className="text-sm font-medium">State</label>
                <select
                  id="state"
                  value={profile.state}
                  onChange={(e) => setProfile({ ...profile, state: e.target.value })}
                  className="rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  aria-required="true"
                >
                  <option value="">Select State</option>
                  {["Rajasthan","Maharashtra","Kerala","Uttar Pradesh","Bihar","West Bengal","Karnataka","Tamil Nadu","Gujarat","Punjab"].map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>

              {/* Occupation */}
              <div className="flex flex-col gap-1">
                <label htmlFor="occupation" className="text-sm font-medium">Occupation</label>
                <select
                  id="occupation"
                  value={profile.occupation}
                  onChange={(e) => setProfile({ ...profile, occupation: e.target.value })}
                  className="rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  aria-required="true"
                >
                  <option value="">Select Occupation</option>
                  {["Farmer","Student","Small Business Owner","Salaried Employee","Self-Employed","Unemployed","Homemaker"].map(o => (
                    <option key={o} value={o}>{o}</option>
                  ))}
                </select>
              </div>

              {/* Income */}
              <div className="flex flex-col gap-1">
                <label htmlFor="income" className="text-sm font-medium">Annual Income</label>
                <select
                  id="income"
                  value={profile.income}
                  onChange={(e) => setProfile({ ...profile, income: e.target.value })}
                  className="rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  aria-required="true"
                >
                  <option value="">Select Income Range</option>
                  <option value="below 1 lakh">Below ₹1 Lakh</option>
                  <option value="1-3 lakh">₹1 – 3 Lakh</option>
                  <option value="3-8 lakh">₹3 – 8 Lakh</option>
                  <option value="above 8 lakh">Above ₹8 Lakh</option>
                </select>
              </div>

              {/* Gender */}
              <div className="flex flex-col gap-1">
                <label htmlFor="gender" className="text-sm font-medium">Gender</label>
                <select
                  id="gender"
                  value={profile.gender}
                  onChange={(e) => setProfile({ ...profile, gender: e.target.value })}
                  className="rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  aria-required="true"
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              {/* Category */}
              <div className="flex flex-col gap-1">
                <label htmlFor="category" className="text-sm font-medium">Social Category</label>
                <select
                  id="category"
                  value={profile.category}
                  onChange={(e) => setProfile({ ...profile, category: e.target.value })}
                  className="rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  aria-required="true"
                >
                  <option value="">Select Category</option>
                  <option value="General">General</option>
                  <option value="OBC">OBC</option>
                  <option value="SC">SC</option>
                  <option value="ST">ST</option>
                  <option value="Minority">Minority</option>
                </select>
              </div>

              <div className="flex items-end">
                <Button
                  type="submit"
                  disabled={loadingRecs}
                  className="w-full gap-2"
                  aria-label="Find government schemes matching your profile"
                >
                  <Search className="h-4 w-4" aria-hidden="true" />
                  {loadingRecs ? "Finding Schemes…" : "Find My Schemes"}
                </Button>
              </div>
            </form>

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div className="mt-6 space-y-3" aria-live="polite" aria-label="Recommended schemes">
                <h2 className="text-sm font-semibold text-primary uppercase tracking-wide">
                  AI-Recommended Schemes for You
                </h2>
                {recommendations.map((rec, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-lg border bg-background/50 hover:bg-muted/50 transition-colors"
                  >
                    <p className="text-sm">{rec.content}</p>
                    <span className="text-xs text-green-500 mt-1 block">
                      {Math.round((1 - rec.score) * 100)}% match
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Main grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Scheme Cards */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" aria-hidden="true" />
                Popular Schemes
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                { name: "PM Kisan Samman Nidhi", match: "92%", href: "https://pmkisan.gov.in" },
                { name: "Stand-Up India", match: "85%", href: "https://www.standupmitra.in" },
                { name: "PMAY Housing", match: "78%", href: "https://pmaymis.gov.in" },
              ].map((scheme) => (
                <a
                  key={scheme.name}
                  href={scheme.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block p-3 rounded-lg border bg-background/50 hover:bg-muted/50 transition-colors focus:outline-none focus:ring-2 focus:ring-primary"
                  aria-label={`${scheme.name} — ${scheme.match} match. Opens official website in new tab.`}
                >
                  <h3 className="font-semibold text-sm">{scheme.name}</h3>
                  <p className="text-xs text-muted-foreground mt-1">{scheme.match} Match based on profile.</p>
                </a>
              ))}
            </CardContent>
          </Card>
        </motion.div>

        {/* Complaints Tracker */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }}>
          <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-orange-500" aria-hidden="true" />
                Active Complaints
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div role="status" aria-label="Complaint: Pothole on Main Road, status: In Progress, 60% resolved">
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">Pothole on Main Road</span>
                  <span className="text-blue-500 text-xs px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20">
                    In Progress
                  </span>
                </div>
                <div
                  className="h-2 w-full bg-muted rounded-full overflow-hidden"
                  role="progressbar"
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={60}
                  aria-label="Resolution progress: 60%"
                >
                  <div className="h-full bg-blue-500 w-[60%]" />
                </div>
                <p className="text-xs text-muted-foreground text-right mt-1">Est. Resolution: 2 Days</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Document Vault */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.2 }}>
          <Card className="bg-card/50 backdrop-blur-md border-white/10 shadow-lg h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-purple-500" aria-hidden="true" />
                Smart Document Vault
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-lg border bg-background/50">
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded bg-primary/10 flex items-center justify-center text-primary font-bold text-xs" aria-hidden="true">PDF</div>
                  <div>
                    <p className="text-sm font-medium">Aadhaar Card</p>
                    <p className="text-[10px] text-green-500">Verified</p>
                  </div>
                </div>
                <CheckCircle2 className="h-4 w-4 text-green-500" aria-label="Verified" />
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg border border-orange-500/30 bg-orange-500/5">
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded bg-orange-500/10 flex items-center justify-center text-orange-500 font-bold text-xs" aria-hidden="true">JPG</div>
                  <div>
                    <p className="text-sm font-medium">Driving License</p>
                    <p className="text-[10px] text-orange-500">Expires in 14 days</p>
                  </div>
                </div>
                <AlertCircle className="h-4 w-4 text-orange-500" aria-label="Warning: expires soon" />
              </div>

              {/* Upload new document */}
              <div className="pt-2">
                <label
                  htmlFor="doc-upload"
                  className="flex items-center gap-2 justify-center w-full py-2 px-3 border border-dashed border-primary/30 rounded-lg cursor-pointer hover:bg-primary/5 transition-colors focus-within:ring-2 focus-within:ring-primary text-sm text-muted-foreground"
                  aria-label="Upload a document for AI verification"
                >
                  <Upload className="h-4 w-4" aria-hidden="true" />
                  Upload Document for Verification
                </label>
                <input
                  id="doc-upload"
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="sr-only"
                  onChange={handleDocumentUpload}
                  aria-label="Select a document image to upload for verification"
                />
                {uploadStatus && (
                  <p
                    className="text-xs mt-2 text-center text-muted-foreground"
                    aria-live="polite"
                    role="status"
                  >
                    {uploadStatus}
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}
