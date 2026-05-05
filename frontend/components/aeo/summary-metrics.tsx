'use client'

import { TrendingUp, TrendingDown, Minus, Bot, Target, Users } from 'lucide-react'
import type { APIResponse } from '@/lib/types'

interface SummaryMetricsProps {
  data: APIResponse
  competitorAvg?: number
}

function getScoreColor(score: number) {
  if (score >= 7) return 'text-emerald-400'
  if (score >= 4) return 'text-amber-400'
  return 'text-red-400'
}

function getScoreBgColor(score: number) {
  if (score >= 7) return 'bg-emerald-500/10 border-emerald-500/20'
  if (score >= 4) return 'bg-amber-500/10 border-amber-500/20'
  return 'bg-red-500/10 border-red-500/20'
}

export function SummaryMetrics({ data, competitorAvg }: SummaryMetricsProps) {
  const mentionedCount = Object.values(data.results).filter(
    (r) => r.analysis.mentioned
  ).length
  
  const delta = competitorAvg !== undefined ? data.avg_score - competitorAvg : null
  
  const metrics = [
    {
      label: 'Overall AEO Score',
      value: data.avg_score.toFixed(1),
      suffix: '/10',
      icon: Target,
      colorClass: getScoreColor(data.avg_score),
      bgClass: getScoreBgColor(data.avg_score),
    },
    {
      label: 'AI Models Queried',
      value: '3',
      suffix: '',
      icon: Bot,
      colorClass: 'text-purple-400',
      bgClass: 'bg-purple-500/10 border-purple-500/20',
    },
    {
      label: 'Mentioned In',
      value: `${mentionedCount}/3`,
      suffix: ' models',
      icon: Users,
      colorClass: mentionedCount >= 2 ? 'text-emerald-400' : mentionedCount === 1 ? 'text-amber-400' : 'text-red-400',
      bgClass: mentionedCount >= 2 ? 'bg-emerald-500/10 border-emerald-500/20' : mentionedCount === 1 ? 'bg-amber-500/10 border-amber-500/20' : 'bg-red-500/10 border-red-500/20',
    },
    {
      label: 'vs Competitor',
      value: delta !== null ? (delta >= 0 ? `+${delta.toFixed(1)}` : delta.toFixed(1)) : 'N/A',
      suffix: '',
      icon: delta !== null ? (delta > 0 ? TrendingUp : delta < 0 ? TrendingDown : Minus) : Minus,
      colorClass: delta !== null ? (delta > 0 ? 'text-emerald-400' : delta < 0 ? 'text-red-400' : 'text-muted-foreground') : 'text-muted-foreground',
      bgClass: delta !== null ? (delta > 0 ? 'bg-emerald-500/10 border-emerald-500/20' : delta < 0 ? 'bg-red-500/10 border-red-500/20' : 'bg-secondary border-border') : 'bg-secondary border-border',
    },
  ]

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric) => (
        <div
          key={metric.label}
          className={`relative overflow-hidden rounded-[20px] border p-5 transition-all duration-300 hover:scale-[1.02] ${metric.bgClass}`}
        >
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">{metric.label}</p>
              <div className="flex items-baseline gap-1">
                <span className={`text-3xl font-bold tracking-tight ${metric.colorClass}`}>
                  {metric.value}
                </span>
                {metric.suffix && (
                  <span className="text-sm text-muted-foreground">{metric.suffix}</span>
                )}
              </div>
            </div>
            <div className={`p-2 rounded-lg ${metric.bgClass}`}>
              <metric.icon className={`h-5 w-5 ${metric.colorClass}`} />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
