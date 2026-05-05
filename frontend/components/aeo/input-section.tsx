'use client'

import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Search, Loader2 } from 'lucide-react'

interface InputSectionProps {
  query: string
  setQuery: (value: string) => void
  brand: string
  setBrand: (value: string) => void
  competitor: string
  setCompetitor: (value: string) => void
  onSubmit: () => void
  isLoading: boolean
}

export function InputSection({
  query,
  setQuery,
  brand,
  setBrand,
  competitor,
  setCompetitor,
  onSubmit,
  isLoading,
}: InputSectionProps) {
  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="crimson-glow-border p-6 md:p-8">
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">
                Customer Query
              </label>
              <Input
                placeholder="best niacinamide serum for oily skin"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="bg-[#111118] border-[#27272a] h-12 rounded-xl focus:border-red-500/50 focus:ring-red-500/20 transition-all text-gray-100 placeholder:text-gray-500"
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">
                Your Brand
              </label>
              <Input
                placeholder="The Ordinary"
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
                className="bg-[#111118] border-[#27272a] h-12 rounded-xl focus:border-red-500/50 focus:ring-red-500/20 transition-all text-gray-100 placeholder:text-gray-500"
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">
                Competitor <span className="text-gray-600">(optional)</span>
              </label>
              <Input
                placeholder="CeraVe"
                value={competitor}
                onChange={(e) => setCompetitor(e.target.value)}
                className="bg-[#111118] border-[#27272a] h-12 rounded-xl focus:border-red-500/50 focus:ring-red-500/20 transition-all text-gray-100 placeholder:text-gray-500"
              />
            </div>
          </div>
          
          <Button
            onClick={onSubmit}
            disabled={isLoading || !query.trim() || !brand.trim()}
            className="w-full h-14 text-lg font-semibold rounded-xl crimson-btn text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Querying 3 AI models in parallel...
              </>
            ) : (
              <>
                <Search className="mr-2 h-5 w-5" />
                Generate Report Card
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}
