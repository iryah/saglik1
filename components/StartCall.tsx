// components/StartCall.tsx
"use client";

import { useVoice } from "@humeai/voice-react";
import { Button } from "@/components/ui/button";
import { Mic } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function StartCall() {
  const { status, connect } = useVoice();

  if (status.value === "connected") return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center p-4"
      >
        <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-6 text-center">
          <h2 className="text-2xl font-bold mb-4">Ready for Your English Lesson?</h2>
          <p className="text-gray-600 mb-8">
            You can practice speaking, improve pronunciation, and have natural conversations with your AI teacher.
          </p>
          
          <div className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-600">
              <p className="font-medium mb-2">Try saying:</p>
              <ul className="space-y-2">
                <li>"Hello, I want to practice English"</li>
                <li>"Can you help me with pronunciation?"</li>
                <li>"Let's have a conversation"</li>
              </ul>
            </div>

            <Button
              size="lg"
              className="w-full"
              onClick={() => {
                connect()
                  .then(() => console.log("Connected"))
                  .catch(console.error);
              }}
            >
              <Mic className="w-4 h-4 mr-2" />
              Start Speaking Practice
            </Button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
