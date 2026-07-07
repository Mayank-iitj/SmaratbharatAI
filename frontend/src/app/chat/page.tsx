"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Bot, User, Mic, Paperclip } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  agent?: string;
  suggested_actions?: string[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Namaste! I am your SmartBharat AI Companion. I can help you with government schemes, complaints, and policy questions. How can I assist you today?",
      agent: "companion",
      suggested_actions: ["Find Schemes for Students", "Report a Pothole", "Explain PMAY"]
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = { id: Date.now().toString(), role: "user", content: text };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, user_id: "user_123" })
      });
      
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        agent: data.agent,
        suggested_actions: data.suggested_actions
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I am having trouble connecting to the servers right now.",
        agent: "system"
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] p-4 max-w-4xl mx-auto w-full z-10">
      <Card className="flex-1 flex flex-col overflow-hidden bg-card/60 backdrop-blur-xl border-white/10 shadow-2xl rounded-2xl">
        <div className="p-4 border-b border-border/50 bg-background/50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10 border border-primary/20 bg-primary/10">
              <Bot className="h-6 w-6 m-auto text-primary" />
            </Avatar>
            <div>
              <h2 className="font-semibold text-lg">Civic Companion</h2>
              <p className="text-xs text-muted-foreground">Always ready to help</p>
            </div>
          </div>
        </div>

        <ScrollArea className="flex-1 p-4" ref={scrollRef}>
          <div className="space-y-6">
            {messages.map((msg, i) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex gap-3 max-w-[80%] ${msg.role === "user" ? "ml-auto flex-row-reverse" : ""}`}
              >
                <Avatar className="h-8 w-8 mt-1 shrink-0">
                  {msg.role === "assistant" ? (
                    <div className="bg-primary/20 w-full h-full flex items-center justify-center text-primary">
                      <Bot size={16} />
                    </div>
                  ) : (
                    <div className="bg-secondary w-full h-full flex items-center justify-center">
                      <User size={16} />
                    </div>
                  )}
                </Avatar>
                
                <div className={`flex flex-col gap-2 ${msg.role === "user" ? "items-end" : "items-start"}`}>
                  <div
                    className={`p-3 rounded-2xl ${
                      msg.role === "user"
                        ? "bg-primary text-primary-foreground rounded-tr-none"
                        : "bg-muted text-foreground rounded-tl-none border border-border/50 shadow-sm"
                    }`}
                  >
                    <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                  </div>
                  
                  {msg.suggested_actions && (
                    <div className="flex flex-wrap gap-2 mt-1">
                      {msg.suggested_actions.map(action => (
                        <Badge 
                          key={action} 
                          variant="outline" 
                          className="cursor-pointer hover:bg-primary/10 transition-colors"
                          onClick={() => handleSend(action)}
                        >
                          {action}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
            {isLoading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
                <Avatar className="h-8 w-8 shrink-0 bg-primary/20 flex items-center justify-center text-primary">
                  <Bot size={16} />
                </Avatar>
                <div className="p-4 rounded-2xl bg-muted rounded-tl-none flex items-center gap-1.5 h-[44px]">
                  <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </motion.div>
            )}
          </div>
        </ScrollArea>

        <div className="p-4 bg-background/50 border-t border-border/50">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend(input);
            }}
            className="flex items-center gap-2 relative"
          >
            <Button type="button" variant="ghost" size="icon" className="text-muted-foreground shrink-0 rounded-full hover:bg-muted">
              <Paperclip className="h-5 w-5" />
            </Button>
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about government services..."
              className="flex-1 rounded-full border-primary/20 bg-background/50 focus-visible:ring-1 focus-visible:ring-primary h-12 px-4 shadow-sm"
            />
            <Button type="button" variant="ghost" size="icon" className="absolute right-14 text-muted-foreground rounded-full hover:bg-muted">
              <Mic className="h-5 w-5" />
            </Button>
            <Button type="submit" disabled={!input.trim() || isLoading} className="rounded-full h-12 w-12 shrink-0 shadow-md">
              <Send className="h-5 w-5 ml-1" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
}

function Badge({ children, className, variant, onClick }: any) {
  return (
    <span onClick={onClick} className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 ${className}`}>
      {children}
    </span>
  )
}
