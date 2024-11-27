// components/Messages.tsx
"use client";

import { useVoice } from "@humeai/voice-react";
import { motion } from "framer-motion";
import { ComponentRef, forwardRef } from "react";

const Messages = forwardRef<
  ComponentRef<typeof motion.div>,
  Record<never, never>
>(function Messages(_, ref) {
  const { messages } = useVoice();

  return (
    <motion.div
      layoutScroll
      className="grow rounded-md overflow-auto p-4"
      ref={ref}
    >
      <div className="max-w-2xl mx-auto w-full flex flex-col gap-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <h2 className="text-xl font-semibold mb-2">Welcome to Your English Lesson!</h2>
            <p>Start the conversation by clicking the button below.</p>
          </div>
        )}
        
        {messages.map((msg, index) => (
          <motion.div
            key={msg.type + index}
            className={`p-4 rounded-lg ${
              msg.type === "user_message" 
                ? "bg-blue-50 ml-auto max-w-[80%]" 
                : "bg-white max-w-[80%]"
            }`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="text-sm text-gray-500 mb-2">
              {msg.type === "user_message" ? "You" : "Teacher"}
            </div>
            <div className="text-gray-800">{msg.message.content}</div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
});

export default Messages;
