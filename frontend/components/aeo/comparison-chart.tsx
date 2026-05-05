'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts'
import type { APIResponse } from '@/lib/types'
import { MODEL_ORDER, MODEL_CONFIGS } from '@/lib/types'

interface ComparisonChartProps {
  data: APIResponse
  brandName: string
  competitorName?: string
}

export function ComparisonChart({ data, brandName, competitorName }: ComparisonChartProps) {
  const chartData = MODEL_ORDER.map((modelName) => {
    const result = data.results[modelName]
    return {
      model: modelName.split(' ')[0], // Shortened name for chart
      fullName: modelName,
      [brandName]: result?.analysis?.score ?? 0,
      ...(competitorName && result?.competitor_analysis ? { [competitorName]: result.competitor_analysis.score } : {}),
    }
  })

  const hasCompetitor = competitorName && Object.values(data.results).some(r => r.competitor_analysis)

  return (
    <div className="relative overflow-hidden rounded-[24px] bg-[#111118] border border-[#27272a] p-6">
      <h3 className="text-lg font-semibold text-foreground mb-2">Model Comparison</h3>
      <p className="text-sm text-muted-foreground mb-4">
        {hasCompetitor ? `${brandName} vs ${competitorName} across AI models` : 'Your brand score across AI models'}
      </p>
      
      <div className="h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} barGap={8}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
            <XAxis 
              dataKey="model" 
              stroke="#71717a" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              domain={[0, 10]} 
              stroke="#71717a" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
              ticks={[0, 2, 4, 6, 8, 10]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#111118',
                border: '1px solid #27272a',
                borderRadius: '12px',
                boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
              }}
              labelStyle={{ color: '#f5f5f7', fontWeight: 600 }}
              itemStyle={{ color: '#a1a1aa' }}
              cursor={{ fill: 'rgba(255,255,255,0.05)' }}
            />
            <Legend 
              wrapperStyle={{ paddingTop: '20px' }}
              formatter={(value) => <span style={{ color: '#a1a1aa' }}>{value}</span>}
            />
            <Bar 
              dataKey={brandName} 
              radius={[6, 6, 0, 0]}
              maxBarSize={40}
            >
              {chartData.map((entry, index) => {
                const config = MODEL_CONFIGS[entry.fullName]
                return (
                  <Cell 
                    key={`brand-cell-${index}`} 
                    fill={config?.scoreColor || '#a855f7'} 
                  />
                )
              })}
            </Bar>
            {hasCompetitor && (
              <Bar 
                dataKey={competitorName} 
                fill="#6b7280" 
                radius={[6, 6, 0, 0]}
                maxBarSize={40}
              />
            )}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
