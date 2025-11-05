import React from "react";
import { CFGRules } from "../components/visualizer/CFGRules";

export const GrammarPage: React.FC = () => {
  return (
    <div className="min-h-screen px-6 py-8 lg:px-8">
      <div className="mx-auto max-w-4xl space-y-8">
        <div className="text-center space-y-4 opacity-0 animate-fade-in">
          <h1 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent">
            CFG Visualizer
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Interactive visualization of Context-Free Grammar rules for HTTP GET request validation
          </p>
        </div>

        <div className="opacity-0 animate-fade-in-delayed">
          <CFGRules />
        </div>
      </div>
    </div>
  );
};