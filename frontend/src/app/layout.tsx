import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SmartBharat AI - One AI Companion for Every Government Service",
  description:
    "India's first AI-Powered Civic Operating System. Discover government schemes, file complaints, simplify policies, and automate paperwork.",
  keywords: "India, government schemes, AI, civic, complaints, Aadhaar, PMAY, PM Kisan",
  authors: [{ name: "SmartBharat AI Team" }],
  openGraph: {
    title: "SmartBharat AI",
    description: "One AI Companion for Every Government Service",
    type: "website",
    locale: "en_IN",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" dir="ltr" className="dark">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#0f0f23" />
      </head>
      <body
        className={`${inter.className} min-h-screen bg-background text-foreground antialiased`}
      >
        {/* Skip navigation link for screen readers */}
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground focus:rounded-md focus:ring-2 focus:ring-white"
        >
          Skip to main content
        </a>

        <div className="relative flex min-h-screen flex-col">
          {/* Animated Background Gradients */}
          <div
            className="fixed inset-0 -z-10 bg-background overflow-hidden"
            aria-hidden="true"
          >
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-500/20 blur-[120px]" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-500/20 blur-[120px]" />
          </div>

          <main id="main-content" role="main" tabIndex={-1}>
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
