// Parse Tree Visualization component - Pixel perfect design with enhanced tree structure

import React from 'react';
import type { ParseTree } from '../types/index';

interface ParseTreeVisualizationProps {
  parseTree: ParseTree;
}

export const ParseTreeVisualization: React.FC<ParseTreeVisualizationProps> = ({ 
  parseTree
}) => {
  const generateColoredTreeHtml = (node: ParseTree, prefix: string = '', isLast: boolean = true, depth: number = 0): string => {
    if (!node) return '';
    
    let result = '';
    const connector = isLast ? '└─ ' : '├─ ';
    const childPrefix = isLast ? '   ' : '│  ';
    
    // Add the current node with enhanced styling
    if (prefix === '') {
      // Root node - styled in blue with bold formatting
      result += `<div class="flex items-center py-1"><span class="text-blue-700 font-bold text-lg bg-blue-50 px-2 py-1 rounded border border-blue-200">${node.label}</span></div>\n`;
    } else {
      // Add terminal value if it's a leaf node
      if (!node.children || node.children.length === 0) {
        result += `<div class="flex items-center py-1"><span class="text-gray-400 font-mono">${prefix}${connector}</span><span class="text-green-700 font-mono font-semibold bg-green-50 px-2 py-1 rounded border border-green-200">"${node.label}"</span></div>\n`;
      } else {
        // Non-terminal node with enhanced styling
        result += `<div class="flex items-center py-1"><span class="text-gray-400 font-mono">${prefix}${connector}</span><span class="text-purple-700 font-bold bg-purple-50 px-2 py-1 rounded border border-purple-200">${node.label}</span></div>\n`;
      }
    }
    
    // Add children
    if (node.children && node.children.length > 0) {
      node.children.forEach((child: ParseTree, index: number) => {
        const isLastChild = index === node.children!.length - 1;
        const newPrefix = prefix === '' ? '' : prefix + childPrefix;
        result += generateColoredTreeHtml(child, newPrefix, isLastChild, depth + 1);
      });
    }
    
    return result;
  };

  const coloredTreeHtml = generateColoredTreeHtml(parseTree);

  if (!parseTree) {
    return (
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
          <h3 className="text-lg font-bold text-gray-900">Parse Tree Structure</h3>
        </div>
        <div className="text-center py-12 text-gray-500">
          <div className="mb-4">
            <svg className="mx-auto h-16 w-16 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h12a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1V8z" clipRule="evenodd" />
            </svg>
          </div>
          <p className="text-lg font-medium mb-2">No parse tree available</p>
          <p className="text-sm">Submit a valid request to see the parse tree structure</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      {/* Enhanced Header */}
      <div className="bg-gradient-to-r from-slate-50 to-slate-100 px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Parse Tree Structure</h3>
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-700 rounded border border-blue-200"></div>
              <span className="text-gray-600">Root</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-purple-700 rounded border border-purple-200"></div>
              <span className="text-gray-600">Non-terminal</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-700 rounded border border-green-200"></div>
              <span className="text-gray-600">Terminal</span>
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Tree Content */}
      <div className="p-6">
        <div className="bg-gradient-to-br from-gray-50 to-white rounded-lg p-6 border border-gray-100 shadow-inner">
          <div className="overflow-x-auto">
            <div 
              className="font-mono text-sm leading-relaxed whitespace-pre-wrap min-w-max"
              dangerouslySetInnerHTML={{ __html: coloredTreeHtml }}
            />
          </div>
        </div>
        
        {/* Tree Statistics */}
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
              <div className="text-lg font-bold text-blue-700">
                {parseTree ? getNodeCount(parseTree) : 0}
              </div>
              <div className="text-xs text-blue-600 font-medium">Total Nodes</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-3 border border-purple-200">
              <div className="text-lg font-bold text-purple-700">
                {parseTree ? getNonTerminalCount(parseTree) : 0}
              </div>
              <div className="text-xs text-purple-600 font-medium">Non-terminals</div>
            </div>
            <div className="bg-green-50 rounded-lg p-3 border border-green-200">
              <div className="text-lg font-bold text-green-700">
                {parseTree ? getTerminalCount(parseTree) : 0}
              </div>
              <div className="text-xs text-green-600 font-medium">Terminals</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper functions for tree statistics
function getNodeCount(node: ParseTree): number {
  if (!node) return 0;
  let count = 1;
  if (node.children) {
    count += node.children.reduce((sum, child) => sum + getNodeCount(child), 0);
  }
  return count;
}

function getNonTerminalCount(node: ParseTree): number {
  if (!node) return 0;
  let count = 0;
  if (node.children && node.children.length > 0) {
    count = 1; // This node is a non-terminal
    count += node.children.reduce((sum, child) => sum + getNonTerminalCount(child), 0);
  }
  return count;
}

function getTerminalCount(node: ParseTree): number {
  if (!node) return 0;
  if (!node.children || node.children.length === 0) {
    return 1; // This is a terminal
  }
  return node.children.reduce((sum, child) => sum + getTerminalCount(child), 0);
}