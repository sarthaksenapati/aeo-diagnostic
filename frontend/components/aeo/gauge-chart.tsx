'use client'

import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

interface GaugeChartProps {
  score: number
}

export function GaugeChart({ score }: GaugeChartProps) {
  // Gauge configuration
  const maxScore = 10
  const normalizedScore = Math.min(Math.max(score, 0), maxScore)
  const percentage = (normalizedScore / maxScore) * 100
  
  // Create gauge data - using a semi-circle approach
  const gaugeData = [
    { value: percentage, color: getScoreColor(score) },
    { value: 100 - percentage, color: '#1a1a24' },
  ]
  
  function getScoreColor(score: number) {
    if (score >= 7) return '#10b981'
    if (score >= 4) return '#f59e0b'
    return '#ef4444'
  }
  
  function getScoreLabel(score: number) {
    if (score >= 7) return 'Excellent'
    if (score >= 4) return 'Moderate'
    return 'Needs Work'
  }

  return (
    <div className="relative overflow-hidden rounded-[24px] bg-[#111118] border border-[#27272a] p-6">
      <h3 className="text-lg font-semibold text-foreground mb-2">Overall AEO Score</h3>
      <p className="text-sm text-muted-foreground mb-4">Your AI visibility rating</p>
      
      <div className="relative h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={gaugeData}
              cx="50%"
              cy="75%"
              startAngle={180}
              endAngle={0}
              innerRadius="60%"
              outerRadius="90%"
              paddingAngle={0}
              dataKey="value"
              stroke="none"
            >
              {gaugeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        
        {/* Score display in center */}
        <div className="absolute inset-x-0 bottom-4 flex flex-col items-center">
          <span 
            className="text-5xl font-bold"
            style={{ color: getScoreColor(score) }}
          >
            {score.toFixed(1)}
          </span>
          <span className="text-gray-500 text-sm">/10</span>
          <span 
            className="text-sm font-medium mt-1"
            style={{ color: getScoreColor(score) }}
          >
            {getScoreLabel(score)}
          </span>
        </div>
      </div>
      
      {/* Score zones legend */}
      <div className="flex justify-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500" />
          <span className="text-xs text-muted-foreground">0-4</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-amber-500" />
          <span className="text-xs text-muted-foreground">4-7</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-emerald-500" />
          <span className="text-xs text-muted-foreground">7-10</span>
        </div>
      </div>
    </div>
  )
}
