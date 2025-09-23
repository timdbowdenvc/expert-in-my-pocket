"use client";

import { Target, ListChecks, CheckCircle } from "lucide-react";

/**
 * EmptyState - Expert In My Pocket welcome screen
 * Extracted from ChatMessagesView empty state section
 * Displays when no messages exist in the current session
 */
export function EmptyState(): React.JSX.Element {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-4 text-center min-h-[60vh]">
      <div className="max-w-4xl w-full space-y-8">
        {/* Main header */}
        <div className="space-y-4">
          <div className="flex items-center justify-center space-x-3">
            <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center">
              <Target className="w-6 h-6 text-green-500" />
            </div>
            <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center">
              <ListChecks className="w-6 h-6 text-blue-500" />
            </div>
            <div className="w-12 h-12 bg-purple-500/10 rounded-xl flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-purple-500" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-white">Expert In My Pocket</h1>
          <p className="text-xl text-neutral-300">Your AI-powered study partner for anything.</p>
        </div>

        {/* Description */}
        <div className="space-y-4">
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Get help with revision, practice questions, and understanding key concepts.
          </p>
        </div>

        {/* Feature highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
          <div className="space-y-3">
            <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center mx-auto">
              <Target className="w-6 h-6 text-green-500" />
            </div>
            <h3 className="font-semibold text-blue-400">Internal Research</h3>
            <p className="text-sm text-neutral-400">
              Query Company Documents.
            </p>
          </div>
          <div className="space-y-3">
            <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center mx-auto">
              <ListChecks className="w-6 h-6 text-blue-500" />
            </div>
            <h3 className="font-semibold text-blue-400">Market Research</h3>
            <p className="text-sm text-neutral-400">
              Generate competitive analysis.
            </p>
          </div>
          <div className="space-y-3">
            <div className="w-12 h-12 bg-purple-500/10 rounded-xl flex items-center justify-center mx-auto">
              <CheckCircle className="w-6 h-6 text-purple-500" />
            </div>
            <h3 className="font-semibold text-purple-400">Key Concept Explanations</h3>
            <p className="text-sm text-neutral-400">
              Get clear explanations of difficult concepts.
            </p>
          </div>
        </div>

        {/* Try asking about section */}
        <div className="space-y-4">
          <p className="text-neutral-400">Try asking for:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              A summary of the Digital T-Level
            </span>
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              Practice questions for the Health T-Level
            </span>
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              An explanation of core concepts in the Construction T-Level
            </span>
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              Help with my revision schedule
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
