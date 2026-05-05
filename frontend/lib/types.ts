export interface Analysis {
  score: number
  rank: 'Top' | 'Middle' | 'Late' | 'Not mentioned'
  sentiment: 'Positive' | 'Neutral' | 'Negative'
  sentiment_emoji: string
  mentioned: boolean
}

export interface ModelResult {
  response: string
  analysis: Analysis
  competitor_analysis?: Analysis
}

export interface APIResponse {
  results: Record<string, ModelResult>
  avg_score: number
  recommendations: string[]
}

export type ModelTheme = 'silver' | 'orange' | 'blue'

export interface ModelCardConfig {
  name: string
  theme: ModelTheme
  gradient: string
  scoreColor: string
  shadow: string
  shadowHover: string
  pillBg: string
  pillText: string
  borderColor: string
}

export const MODEL_CONFIGS: Record<string, ModelCardConfig> = {
  'Gemma 3 27B': {
    name: 'Gemma 3 27B',
    theme: 'silver',
    gradient: 'linear-gradient(90deg, #9ca3af, #e5e7eb, #9ca3af)',
    scoreColor: '#e5e7eb',
    shadow: '0 0 20px rgba(156,163,175,0.15)',
    shadowHover: '0 0 30px rgba(156,163,175,0.3)',
    pillBg: 'rgba(156,163,175,0.15)',
    pillText: '#e5e7eb',
    borderColor: '#9ca3af',
  },
  'Nemotron 3 Super': {
    name: 'Nemotron 3 Super',
    theme: 'orange',
    gradient: 'linear-gradient(90deg, #f97316, #fb923c, #fbbf24)',
    scoreColor: '#f97316',
    shadow: '0 0 20px rgba(249,115,22,0.15)',
    shadowHover: '0 0 30px rgba(249,115,22,0.3)',
    pillBg: 'rgba(249,115,22,0.15)',
    pillText: '#fb923c',
    borderColor: '#f97316',
  },
  'GPT OSS 120B': {
    name: 'GPT OSS 120B',
    theme: 'blue',
    gradient: 'linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd)',
    scoreColor: '#60a5fa',
    shadow: '0 0 20px rgba(59,130,246,0.15)',
    shadowHover: '0 0 30px rgba(59,130,246,0.3)',
    pillBg: 'rgba(59,130,246,0.15)',
    pillText: '#60a5fa',
    borderColor: '#3b82f6',
  },
}

export const MODEL_ORDER = ['Gemma 3 27B', 'Nemotron 3 Super', 'GPT OSS 120B']
