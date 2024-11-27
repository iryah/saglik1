"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ChevronRight, Star, Zap, Clock, Globe, Users, CheckCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden px-6 pt-16 lg:px-8 lg:pt-32">
        <div className="mx-auto max-w-2xl text-center">
          <div className="mb-8 flex justify-center">
            <div className="rounded-full bg-blue-50 px-3 py-1 text-sm leading-6 text-blue-600 ring-1 ring-inset ring-blue-600/10">
              AI-Powered Learning
            </div>
          </div>
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
            Master English with Your
            <span className="text-blue-600"> Personal AI Teacher</span>
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Practice speaking English naturally with our advanced AI tutor. Get real-time feedback, improve pronunciation, and build confidence.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link href="/practice">
              <Button className="bg-blue-600 hover:bg-blue-700">
                Start Free Lesson <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link href="#how-it-works" className="text-sm font-semibold leading-6 text-gray-900">
              Learn more <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mx-auto mt-16 max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:max-w-none">
            <dl className="grid grid-cols-1 gap-0.5 overflow-hidden rounded-2xl text-center sm:grid-cols-2 lg:grid-cols-4">
              <div className="flex flex-col bg-gray-50 p-8">
                <dt className="text-sm font-semibold leading-6 text-gray-600">Active Students</dt>
                <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900">50K+</dd>
              </div>
              <div className="flex flex-col bg-gray-50 p-8">
                <dt className="text-sm font-semibold leading-6 text-gray-600">Lessons Completed</dt>
                <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900">1M+</dd>
              </div>
              <div className="flex flex-col bg-gray-50 p-8">
                <dt className="text-sm font-semibold leading-6 text-gray-600">Student Rating</dt>
                <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900">4.9/5</dd>
              </div>
              <div className="flex flex-col bg-gray-50 p-8">
                <dt className="text-sm font-semibold leading-6 text-gray-600">Available 24/7</dt>
                <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900">100%</dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-blue-600">Learn Faster</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need to master English
            </p>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Our AI-powered platform provides personalized learning experience tailored to your needs.
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
              <div className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                    <Globe className="h-6 w-6 text-white" />
                  </div>
                  Speaking Practice
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">
                  Natural conversations with AI that understands and responds to your speech.
                </dd>
              </div>
              <div className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                    <Zap className="h-6 w-6 text-white" />
                  </div>
                  Instant Feedback
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">
                  Get real-time corrections and tips to improve your pronunciation.
                </dd>
              </div>
              <div className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                    <Users className="h-6 w-6 text-white" />
                  </div>
                  Personalized Learning
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">
                  Lessons adapted to your level, goals, and learning pace.
                </dd>
              </div>
              <div className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                    <Clock className="h-6 w-6 text-white" />
                  </div>
                  24/7 Availability
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">
                  Practice anytime, anywhere with our always-available AI teacher.
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative isolate overflow-hidden bg-blue-600">
        <div className="px-6 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Start improving your English today.
              <br />
              Try your first lesson for free.
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">
              Join thousands of students who are already improving their English with our AI teacher.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link href="/practice">
                <Button className="bg-white text-blue-600 hover:bg-gray-100">
                  Start Free Lesson
                </Button>
              </Link>
              <Link href="#features">
                <Button variant="outline" className="text-white border-white hover:bg-blue-700">
                  Learn more
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
