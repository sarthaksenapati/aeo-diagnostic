'use client'

import { CheckCircle2, AlertTriangle, XCircle } from 'lucide-react'

interface VerdictBannerProps {
  score: number
}

export function VerdictBanner({ score }: VerdictBannerProps) {
  const getVerdictConfig = () => {
    if (score >= 7) {
      return {
        icon: CheckCircle2,
        message: 'Strong AI visibility — Brand is actively recommended',
        bgClass: 'bg-emerald-500/10 border-emerald-500/30',
        iconClass: 'text-emerald-400',
        textClass: 'text-emerald-300',
      }
    }
    if (score >= 4) {
      return {
        icon: AlertTriangle,
        message: 'Moderate AI visibility — mentioned but not leading',
        bgClass: 'bg-amber-500/10 border-amber-500/30',
        iconClass: 'text-amber-400',
        textClass: 'text-amber-300',
      }
    }
    return {
      icon: XCircle,
      message: 'Low AI visibility — not being recommended',
      bgClass: 'bg-red-500/10 border-red-500/30',
      iconClass: 'text-red-400',
      textClass: 'text-red-300',
    }
  }

  const config = getVerdictConfig()

  return (
    <div
      className={`flex items-center gap-4 p-5 rounded-[20px] border ${config.bgClass} transition-all duration-300`}
    >
      <config.icon className={`h-6 w-6 flex-shrink-0 ${config.iconClass}`} />
      <p className={`text-lg font-medium ${config.textClass}`}>
        {config.message}
      </p>
    </div>
  )
}
