"use client";

import { VoiceProvider } from "@humeai/voice-react";
import { ComponentRef, useRef } from "react";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

// Komponentleri import edelim
import Messages from "@/components/Messages";
import Controls from "@/components/Controls";
import StartCall from "@/components/StartCall";

export default function PracticePage() {
  const timeout = useRef<number | null>(null);
  const ref = useRef<ComponentRef<typeof Messages> | null>(null);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Lesson Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Button>
          </Link>
          <div className="flex items-center space-x-4">
            {/* Lesson Progress */}
            <div className="text-sm text-gray-600">
              Lesson in Progress
            </div>
          </div>
        </div>
      </header>

      {/* Main Practice Area */}
      <div className="flex-1 overflow-hidden relative">
        <VoiceProvider
          auth={{ 
            type: "accessToken", 
            value: process.env.NEXT_PUBLIC_HUME_ACCESS_TOKEN || "" 
          }}
        >
          <div className="absolute inset-0 flex flex-col">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto bg-gray-50">
              <Messages ref={ref} />
            </div>

            {/* Controls Area */}
            <div className="bg-white border-t p-4">
              <Controls />
            </div>

            {/* Start Call Overlay */}
            <StartCall />
          </div>
        </VoiceProvider>
      </div>
    </div>
  );
}
