"use client";

import { useVoice } from "@humeai/voice-react";
import { Button } from "@/components/ui/button";
import { Mic, MicOff, Volume2 } from "lucide-react";

export default function Controls() {
  const { isMuted, mute, unmute } = useVoice();

  return (
    <div className="max-w-2xl mx-auto w-full flex justify-between items-center">
      <div className="flex gap-4 items-center">
        <Button
          onClick={() => isMuted ? unmute() : mute()}
          variant={isMuted ? "outline" : "default"}
          className="flex items-center gap-2"
        >
          {isMuted ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
          {isMuted ? "Unmute Microphone" : "Mute Microphone"}
        </Button>
      </div>

      <div className="flex items-center text-sm text-gray-500">
        <Volume2 className="h-4 w-4 mr-2" />
        Speaking Practice
      </div>
    </div>
  );
}
