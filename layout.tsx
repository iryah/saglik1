import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "English AI Teacher - Learn English with AI",
  description: "Practice English speaking and improve your pronunciation with our AI-powered English teacher",
  keywords: "English learning, AI teacher, pronunciation practice, speaking practice, language learning",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={cn(
        inter.className,
        "min-h-screen antialiased"
      )}>
        {/* Navbar */}
        <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-sm z-50 border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <a href="/" className="text-xl font-bold text-blue-600">
                English AI
              </a>
              <div className="flex items-center gap-4">
                <a href="/practice" className="text-sm font-medium text-gray-700 hover:text-blue-600">
                  Practice
                </a>
                <a href="#features" className="text-sm font-medium text-gray-700 hover:text-blue-600">
                  Features
                </a>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="pt-16">
          {children}
        </main>

        {/* Footer */}
        <footer className="bg-gray-50 border-t">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-lg font-semibold mb-4">English AI Teacher</h3>
                <p className="text-gray-600">Practice English speaking with advanced AI technology.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
                <ul className="space-y-2">
                  <li>
                    <a href="/practice" className="text-gray-600 hover:text-blue-600">
                      Start Practice
                    </a>
                  </li>
                  <li>
                    <a href="#features" className="text-gray-600 hover:text-blue-600">
                      Features
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Contact</h3>
                <p className="text-gray-600">
                  Need help? Contact us at support@englishai.com
                </p>
              </div>
            </div>
            <div className="mt-8 pt-8 border-t text-center text-gray-500">
              <p>&copy; {new Date().getFullYear()} English AI Teacher. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
