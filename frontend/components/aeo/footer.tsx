'use client'

export function Footer() {
  return (
    <footer className="mt-16 pb-8 text-center">
      <p className="text-sm text-muted-foreground">
        AEO Diagnostic • Powered by{' '}
        <span className="text-[#e5e7eb]">Gemma 3 27B</span> ·{' '}
        <span className="text-[#fb923c]">Nemotron 3 Super</span> ·{' '}
        <span className="text-[#60a5fa]">GPT OSS 120B</span>
        {' '}via OpenRouter
      </p>
    </footer>
  )
}
