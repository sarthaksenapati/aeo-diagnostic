'use client'

import { Lightbulb, ArrowRight } from 'lucide-react'

interface RecommendationsProps {
  recommendations: string[]
}

export function Recommendations({ recommendations }: RecommendationsProps) {
  if (!recommendations || recommendations.length === 0) return null

  return (
    <div className="relative overflow-hidden rounded-[24px] bg-[#111118] border border-[#27272a] p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-purple-500/10">
          <Lightbulb className="h-5 w-5 text-purple-400" />
        </div>
        <h3 className="text-lg font-semibold text-foreground">AI Recommendations</h3>
      </div>
      
      <div className="space-y-4">
        {recommendations.map((recommendation, index) => (
          <div
            key={index}
            className="flex items-start gap-4 p-4 rounded-xl bg-[#0a0a0f] border-l-4 border-purple-500 transition-all duration-200 hover:bg-[#0f0f15]"
          >
            <ArrowRight className="h-5 w-5 text-purple-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-foreground leading-relaxed">{recommendation}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
