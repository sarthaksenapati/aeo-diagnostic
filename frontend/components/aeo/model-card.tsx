'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp, Crown } from 'lucide-react'
import type { ModelResult, ModelCardConfig } from '@/lib/types'
import { MODEL_CONFIGS } from '@/lib/types'

interface ModelCardProps {
  modelName: string
  result: ModelResult
  isBest: boolean
  competitorName?: string
}

export function ModelCard({ modelName, result, isBest, competitorName }: ModelCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const config = MODEL_CONFIGS[modelName] || MODEL_CONFIGS['Gemma 3 27B']
  
  const { analysis, competitor_analysis } = result
  
  // Determine competitor comparison
  const getComparisonLabel = () => {
    if (!competitor_analysis) return null
    if (analysis.score > competitor_analysis.score) return 'You lead'
    if (analysis.score < competitor_analysis.score) return 'Competitor leads'
    return 'Tied'
  }
  
  const comparisonLabel = getComparisonLabel()

  const themeStyles = {
    silver: {
      gradient: 'linear-gradient(90deg, #9ca3af, #d1d5db, #e5e7eb, #f3f4f6, #e5e7eb, #d1d5db, #9ca3af)',
      glow: '0 0 40px rgba(156, 163, 175, 0.4), 0 0 80px rgba(229, 231, 235, 0.2)',
    },
    orange: {
      gradient: 'linear-gradient(90deg, #f97316, #fb923c, #fbbf24, #fcd34d, #fbbf24, #fb923c, #f97316)',
      glow: '0 0 40px rgba(249, 115, 22, 0.4), 0 0 80px rgba(251, 191, 36, 0.2)',
    },
    blue: {
      gradient: 'linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd, #bfdbfe, #93c5fd, #60a5fa, #3b82f6)',
      glow: '0 0 40px rgba(59, 130, 246, 0.4), 0 0 80px rgba(147, 197, 253, 0.2)',
    },
  }

  const currentTheme = themeStyles[config.theme]

  return (
    <div 
      className="relative rounded-[24px] p-[2px] transition-all duration-300 hover:-translate-y-1.5 group animate-border-glow"
      style={{
        background: currentTheme.gradient,
        backgroundSize: '300% 100%',
        boxShadow: 'none',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.boxShadow = currentTheme.glow
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.boxShadow = 'none'
      }}
    >
      <div className="bg-[#111118] rounded-[22px] p-6">
        {/* Header with model name and best badge */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground">{modelName}</h3>
          {isBest && (
            <div
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium"
              style={{
                background: config.pillBg,
                color: config.pillText,
                boxShadow: `0 0 12px ${config.borderColor}40`,
              }}
            >
              <Crown className="h-4 w-4" />
              Best
            </div>
          )}
        </div>
        
        {/* Large score display */}
        <div className="mb-6">
          <span
            className="text-6xl font-bold tracking-tight"
            style={{ color: config.scoreColor }}
          >
            {analysis.score.toFixed(1)}
          </span>
          <span className="text-2xl text-muted-foreground ml-1">/10</span>
        </div>
        
        {/* Pills/badges */}
        <div className="flex flex-wrap gap-2 mb-4">
          {/* Rank pill */}
          <span
            className="px-3 py-1.5 rounded-full text-sm font-medium"
            style={{
              background: config.pillBg,
              color: config.pillText,
            }}
          >
            {analysis.rank}
          </span>
          
          {/* Sentiment pill */}
          <span
            className="px-3 py-1.5 rounded-full text-sm font-medium"
            style={{
              background: config.pillBg,
              color: config.pillText,
            }}
          >
            {analysis.sentiment_emoji} {analysis.sentiment}
          </span>
          
          {/* Competitor comparison pill */}
          {comparisonLabel && (
            <span
              className="px-3 py-1.5 rounded-full text-sm font-medium"
              style={{
                background: comparisonLabel === 'You lead' 
                  ? 'rgba(16,185,129,0.15)' 
                  : comparisonLabel === 'Competitor leads'
                  ? 'rgba(239,68,68,0.15)'
                  : config.pillBg,
                color: comparisonLabel === 'You lead'
                  ? '#10b981'
                  : comparisonLabel === 'Competitor leads'
                  ? '#ef4444'
                  : config.pillText,
              }}
            >
              {comparisonLabel}
            </span>
          )}
        </div>
        
        {/* Expandable section */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full flex items-center justify-between py-3 px-4 rounded-xl transition-all duration-200 hover:bg-[#1a1a24]"
          style={{
            border: `1px solid ${config.borderColor}30`,
          }}
        >
          <span className="text-sm font-medium text-muted-foreground">
            Full AI Response
          </span>
          {isExpanded ? (
            <ChevronUp className="h-4 w-4 text-muted-foreground" />
          ) : (
            <ChevronDown className="h-4 w-4 text-muted-foreground" />
          )}
        </button>
        
        {isExpanded && (
          <div
            className="mt-4 p-4 rounded-xl text-sm text-muted-foreground leading-relaxed max-h-[300px] overflow-y-auto"
            style={{
              background: '#0a0a0f',
              border: `1px solid ${config.borderColor}30`,
            }}
          >
            {result.response}
          </div>
        )}
      </div>
    </div>
  )
}
