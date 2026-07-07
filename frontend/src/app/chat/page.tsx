"use client";

import { useState, useRef, useEffect, useCallback, KeyboardEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Mic, Paperclip, X, ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  agent?: string;
  suggested_actions?: string[];
  imagePreview?: string;
}

interface UploadedFile {
  file: File;
  preview: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const INITIAL_MESSAGE: Message = {
  id: "1",
  role: "assistant",
  content:
    "Namaste! 🙏 I am your **SmartBharat AI Companion**. I can help you:\n\n• 🏛️ Discover government schemes you're eligible for\n• 📸 File civic complaints (just upload a photo)\n• 📋 Simplify complex government policies\n• 🆔 Verify documents via OCR\n\nHow can I assist you today?",
  agent: "companion",
  suggested_actions: ["Find Schemes for Farmers", "Report a Pothole", "Explain PMAY", "Student Scholarships"],
};

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([INITIAL_MESSAGE]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [language, setLanguage] = useState<"en" | "hi">("en");
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // -------------------------------------------------------------------------
  // File upload handler
  // -------------------------------------------------------------------------
  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const preview = URL.createObjectURL(file);
    setUploadedFile({ file, preview });
  }, []);

  const handleRemoveFile = useCallback(() => {
    if (uploadedFile) URL.revokeObjectURL(uploadedFile.preview);
    setUploadedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }, [uploadedFile]);

  // -------------------------------------------------------------------------
  // Send message
  // -------------------------------------------------------------------------
  const handleSend = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed && !uploadedFile) return;

      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: trimmed || (uploadedFile ? `[Image: ${uploadedFile.file.name}]` : ""),
        imagePreview: uploadedFile?.preview,
      };

      setMessages((prev) => [...prev, userMessage]);
      setInput("");
      setIsLoading(true);

      try {
        let data: { response: string; agent: string; suggested_actions: string[] };

        if (uploadedFile) {
          // Upload image to complaint analysis endpoint
          const formData = new FormData();
          formData.append("file", uploadedFile.file);
          const res = await fetch(`${API_URL}/api/documents/analyze-complaint`, {
            method: "POST",
            body: formData,
          });
          const rawResult = await res.json();
          data = {
            response:
              rawResult.raw_analysis ||
              rawResult.message ||
              "I've analyzed your image. Please file this as a formal complaint below.",
            agent: "vision",
            suggested_actions: ["File Complaint Now", "Describe Location", "Upload Another Image"],
          };
          handleRemoveFile();
        } else {
          // Chat endpoint
          const res = await fetch(`${API_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: trimmed, user_id: "user_123" }),
          });
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          data = await res.json();
        }

        setMessages((prev) => [
          ...prev,
          {
            id: (Date.now() + 1).toString(),
            role: "assistant",
            content: data.response,
            agent: data.agent,
            suggested_actions: data.suggested_actions,
          },
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            id: (Date.now() + 1).toString(),
            role: "assistant",
            content:
              "Sorry, I am having trouble connecting to the servers right now. Please try again in a moment.",
            agent: "system",
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [uploadedFile, handleRemoveFile]
  );

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend(input);
      }
    },
    [input, handleSend]
  );

  // -------------------------------------------------------------------------
  // Render
  // -------------------------------------------------------------------------
  return (
    <section
      className="flex flex-col h-[calc(100vh-0px)] p-4 max-w-4xl mx-auto w-full z-10"
      aria-label="SmartBharat AI chat interface"
    >
      {/* Language Toggle */}
      <div className="flex justify-end mb-2 gap-2">
        <button
          onClick={() => setLanguage(language === "en" ? "hi" : "en")}
          className="text-xs px-3 py-1 rounded-full border border-primary/20 bg-primary/10 text-primary hover:bg-primary/20 transition-colors focus:outline-none focus:ring-2 focus:ring-primary"
          aria-label={`Switch to ${language === "en" ? "Hindi" : "English"} language`}
        >
          {language === "en" ? "🇮🇳 हिंदी" : "🇬🇧 English"}
        </button>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden bg-card/60 backdrop-blur-xl border-white/10 shadow-2xl rounded-2xl">
        {/* Header */}
        <header className="p-4 border-b border-border/50 bg-background/50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10 border border-primary/20 bg-primary/10" aria-hidden="true">
              <div className="flex items-center justify-center w-full h-full">
                <Bot className="h-6 w-6 text-primary" />
              </div>
            </Avatar>
            <div>
              <h1 className="font-semibold text-lg">
                {language === "en" ? "Civic Companion" : "नागरिक साथी"}
              </h1>
              <p className="text-xs text-muted-foreground flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-green-500 inline-block" aria-hidden="true" />
                {language === "en" ? "Online · Always ready to help" : "ऑनलाइन · हमेशा मदद के लिए"}
              </p>
            </div>
          </div>
        </header>

        {/* Messages */}
        <ScrollArea className="flex-1 p-4" ref={scrollRef}>
          {/* Live region for screen reader announcements */}
          <div
            aria-live="polite"
            aria-atomic="false"
            aria-relevant="additions"
            className="sr-only"
            id="chat-live-region"
          >
            {messages.length > 1 && messages[messages.length - 1].role === "assistant"
              ? messages[messages.length - 1].content
              : ""}
          </div>

          <div className="space-y-6" role="log" aria-label="Chat messages" aria-live="off">
            <AnimatePresence initial={false}>
              {messages.map((msg) => (
                <motion.article
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className={`flex gap-3 max-w-[80%] ${msg.role === "user" ? "ml-auto flex-row-reverse" : ""}`}
                  aria-label={`${msg.role === "user" ? "You" : "SmartBharat AI"}: ${msg.content}`}
                >
                  <div
                    className="h-8 w-8 mt-1 shrink-0 rounded-full flex items-center justify-center"
                    aria-hidden="true"
                  >
                    {msg.role === "assistant" ? (
                      <div className="bg-primary/20 w-8 h-8 rounded-full flex items-center justify-center text-primary">
                        <Bot size={16} />
                      </div>
                    ) : (
                      <div className="bg-secondary w-8 h-8 rounded-full flex items-center justify-center">
                        <User size={16} />
                      </div>
                    )}
                  </div>

                  <div className={`flex flex-col gap-2 ${msg.role === "user" ? "items-end" : "items-start"}`}>
                    {/* Image preview */}
                    {msg.imagePreview && (
                      <img
                        src={msg.imagePreview}
                        alt="Uploaded complaint image"
                        className="max-w-[200px] rounded-xl border border-border/50 mb-1"
                      />
                    )}

                    <div
                      className={`p-3 rounded-2xl ${
                        msg.role === "user"
                          ? "bg-primary text-primary-foreground rounded-tr-none"
                          : "bg-muted text-foreground rounded-tl-none border border-border/50 shadow-sm"
                      }`}
                    >
                      <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                    </div>

                    {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                      <div
                        className="flex flex-wrap gap-2 mt-1"
                        role="group"
                        aria-label="Suggested follow-up actions"
                      >
                        {msg.suggested_actions.map((action) => (
                          <button
                            key={action}
                            onClick={() => handleSend(action)}
                            className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold cursor-pointer hover:bg-primary/10 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1"
                            aria-label={`Send message: ${action}`}
                          >
                            {action}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </motion.article>
              ))}
            </AnimatePresence>

            {/* Loading indicator */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex gap-3"
                aria-label="SmartBharat AI is thinking"
                role="status"
              >
                <div className="bg-primary/20 w-8 h-8 rounded-full flex items-center justify-center text-primary">
                  <Bot size={16} aria-hidden="true" />
                </div>
                <div
                  className="p-4 rounded-2xl bg-muted rounded-tl-none flex items-center gap-1.5 h-[44px]"
                  aria-hidden="true"
                >
                  <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </motion.div>
            )}
          </div>
        </ScrollArea>

        {/* Image preview bar */}
        {uploadedFile && (
          <div className="px-4 py-2 bg-background/50 border-t border-border/50 flex items-center gap-3">
            <ImageIcon className="h-4 w-4 text-primary shrink-0" aria-hidden="true" />
            <img
              src={uploadedFile.preview}
              alt="Selected file preview"
              className="h-10 w-10 rounded object-cover border border-border"
            />
            <span className="text-xs text-muted-foreground truncate flex-1">{uploadedFile.file.name}</span>
            <button
              onClick={handleRemoveFile}
              className="p-1 rounded-full hover:bg-muted focus:outline-none focus:ring-2 focus:ring-primary"
              aria-label="Remove selected image"
            >
              <X className="h-4 w-4 text-muted-foreground" />
            </button>
          </div>
        )}

        {/* Input area */}
        <div className="p-4 bg-background/50 border-t border-border/50">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend(input);
            }}
            className="flex items-center gap-2 relative"
            aria-label="Send a message"
            role="form"
          >
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              className="sr-only"
              onChange={handleFileSelect}
              aria-label="Upload an image for complaint analysis"
              id="file-upload-input"
            />
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="text-muted-foreground shrink-0 rounded-full hover:bg-muted focus-visible:ring-2"
              aria-label="Upload image for AI complaint analysis"
              onClick={() => fileInputRef.current?.click()}
            >
              <Paperclip className="h-5 w-5" aria-hidden="true" />
            </Button>

            <Input
              ref={inputRef}
              id="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                language === "en"
                  ? "Ask anything about government services..."
                  : "सरकारी सेवाओं के बारे में पूछें..."
              }
              className="flex-1 rounded-full border-primary/20 bg-background/50 focus-visible:ring-1 focus-visible:ring-primary h-12 px-4 shadow-sm"
              aria-label="Chat message input"
              aria-describedby="chat-hint"
              disabled={isLoading}
              maxLength={2000}
              autoComplete="off"
            />
            <span id="chat-hint" className="sr-only">
              Type your message and press Enter or click Send to get AI assistance with government services.
            </span>

            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="absolute right-14 text-muted-foreground rounded-full hover:bg-muted focus-visible:ring-2"
              aria-label="Voice input (coming soon)"
              disabled
            >
              <Mic className="h-5 w-5" aria-hidden="true" />
            </Button>

            <Button
              type="submit"
              disabled={(!input.trim() && !uploadedFile) || isLoading}
              className="rounded-full h-12 w-12 shrink-0 shadow-md focus-visible:ring-2 focus-visible:ring-white"
              aria-label="Send message"
              id="send-button"
            >
              <Send className="h-5 w-5 ml-1" aria-hidden="true" />
            </Button>
          </form>
        </div>
      </Card>
    </section>
  );
}
