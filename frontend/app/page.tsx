'use client'

import { useState } from 'react'
import { InputSection } from '@/components/aeo/input-section'
import { SummaryMetrics } from '@/components/aeo/summary-metrics'
import { VerdictBanner } from '@/components/aeo/verdict-banner'
import { GaugeChart } from '@/components/aeo/gauge-chart'
import { ComparisonChart } from '@/components/aeo/comparison-chart'
import { ModelCard } from '@/components/aeo/model-card'
import { Recommendations } from '@/components/aeo/recommendations'
import { Footer } from '@/components/aeo/footer'
import type { APIResponse } from '@/lib/types'
import { MODEL_ORDER } from '@/lib/types'

// Mock data for demonstration
const MOCK_DATA: APIResponse = {
  results: {
    'Gemma 3 27B': {
      response: 'For oily skin looking for a niacinamide serum, The Ordinary Niacinamide 10% + Zinc 1% is an excellent choice. It\'s affordable, effective at controlling sebum production, and helps minimize the appearance of pores. The zinc in the formula adds additional oil-control benefits. This serum has become a cult favorite for good reason - it delivers results without breaking the bank. However, start slowly if you have sensitive skin, as the 10% concentration can be potent for some users.',
      analysis: {
        score: 8.5,
        rank: 'Top',
        sentiment: 'Positive',
        sentiment_emoji: '😊',
        mentioned: true,
      },
      competitor_analysis: {
        score: 6.2,
        rank: 'Middle',
        sentiment: 'Neutral',
        sentiment_emoji: '😐',
        mentioned: true,
      },
    },
    'Nemotron 3 Super': {
      response: 'When it comes to niacinamide serums for oily skin, I\'d recommend considering The Ordinary\'s Niacinamide 10% + Zinc 1%. It\'s a fantastic budget-friendly option that effectively helps regulate oil production and improve skin texture. The formula is lightweight and absorbs quickly without leaving a greasy residue - perfect for oily skin types. Many users report visible improvements in pore appearance and overall skin clarity within weeks of consistent use.',
      analysis: {
        score: 7.8,
        rank: 'Top',
        sentiment: 'Positive',
        sentiment_emoji: '😊',
        mentioned: true,
      },
      competitor_analysis: {
        score: 7.0,
        rank: 'Middle',
        sentiment: 'Positive',
        sentiment_emoji: '😊',
        mentioned: true,
      },
    },
    'GPT OSS 120B': {
      response: 'For those with oily skin seeking a niacinamide serum, The Ordinary offers one of the most popular and cost-effective options on the market. Their Niacinamide 10% + Zinc 1% serum is specifically formulated to help balance visible sebum activity. The high concentration of niacinamide (vitamin B3) works to visibly reduce pore congestion, while zinc PCA helps control oil production. It\'s recommended to use this serum in the morning and/or evening before heavier creams.',
      analysis: {
        score: 8.2,
        rank: 'Top',
        sentiment: 'Positive',
        sentiment_emoji: '😊',
        mentioned: true,
      },
      competitor_analysis: {
        score: 5.5,
        rank: 'Late',
        sentiment: 'Neutral',
        sentiment_emoji: '😐',
        mentioned: true,
      },
    },
  },
  avg_score: 8.17,
  recommendations: [
    'Continue building strong product descriptions that highlight key ingredients like niacinamide and zinc for SEO optimization.',
    'Engage with user-generated content and reviews to increase social proof signals that AI models use for recommendations.',
    'Consider creating comparison content against competitors to help AI models understand your product\'s unique value proposition.',
  ],
}

export default function AEODashboard() {
  const [query, setQuery] = useState('')
  const [brand, setBrand] = useState('')
  const [competitor, setCompetitor] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [data, setData] = useState<APIResponse | null>(null)

  const handleSubmit = async () => {
    setIsLoading(true)
    
    try {
      // Try to fetch from the actual API
      const response = await fetch('https://aeo-diagnostic.onrender.com/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          product: brand,
          competitor: competitor || undefined,
        }),
      })
      
      if (response.ok) {
        const result = await response.json()
        setData(result)
      } else {
        // Fallback to mock data for demo
        await new Promise((resolve) => setTimeout(resolve, 2000))
        setData(MOCK_DATA)
      }
    } catch {
      // Fallback to mock data for demo
      await new Promise((resolve) => setTimeout(resolve, 2000))
      setData(MOCK_DATA)
    }
    
    setIsLoading(false)
  }

  // Calculate competitor average score
  const competitorAvg = data
    ? Object.values(data.results)
        .filter((r) => r.competitor_analysis)
        .reduce((acc, r) => acc + (r.competitor_analysis?.score || 0), 0) /
      Object.values(data.results).filter((r) => r.competitor_analysis).length || undefined
    : undefined

  // Find the best performing model
  const bestModel = data
    ? MODEL_ORDER.reduce((best, model) => {
        const currentScore = data.results[model]?.analysis?.score || 0
        const bestScore = data.results[best]?.analysis?.score || 0
        return currentScore > bestScore ? model : best
      }, MODEL_ORDER[0])
    : null

  return (
    <main className="min-h-screen bg-[#0a0a0f]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-block mb-6">
            <div className="crimson-glow-border px-8 pt-4 pb-5">
              <h1 className="text-4xl md:text-5xl font-bold crimson-text leading-tight">
                AEO Diagnostic
              </h1>
            </div>
          </div>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto text-balance">
            Discover how AI assistants recommend your product. Analyze visibility across ChatGPT, Perplexity, and Gemini.
          </p>
        </div>

        {/* Input Section */}
        <InputSection
          query={query}
          setQuery={setQuery}
          brand={brand}
          setBrand={setBrand}
          competitor={competitor}
          setCompetitor={setCompetitor}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />

        {/* Results Section */}
        {data && (
          <div className="mt-12 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Summary Metrics */}
            <SummaryMetrics data={data} competitorAvg={competitorAvg} />
            
            {/* Verdict Banner */}
            <VerdictBanner score={data.avg_score} />
            
            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <GaugeChart score={data.avg_score} />
              <ComparisonChart 
                data={data} 
                brandName={brand || 'Your Brand'} 
                competitorName={competitor || undefined} 
              />
            </div>
            
            {/* Model Report Cards */}
            <div>
              <h2 className="text-2xl font-bold text-foreground mb-6">Model Report Cards</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {MODEL_ORDER.map((modelName) => {
                  const result = data.results[modelName]
                  if (!result) return null
                  return (
                    <ModelCard
                      key={modelName}
                      modelName={modelName}
                      result={result}
                      isBest={modelName === bestModel}
                      competitorName={competitor || undefined}
                    />
                  )
                })}
              </div>
            </div>
            
            {/* Recommendations */}
            <Recommendations recommendations={data.recommendations} />
          </div>
        )}

        {/* Footer */}
        <Footer />
      </div>
    </main>
  )
}
