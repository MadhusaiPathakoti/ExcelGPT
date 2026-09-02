import { useEffect, useState } from 'react'
import { applyTheme, getInitialTheme } from '../lib/theme'
import type { Theme } from '../lib/theme'

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(() => getInitialTheme())

  useEffect(() => {
    applyTheme(theme)
  }, [theme])

  return (
    <button
      type="button"
      onClick={() => setTheme((current) => (current === 'dark' ? 'light' : 'dark'))}
      aria-label={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
      title={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
      className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-slate-300 bg-white text-sm hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-800 dark:hover:bg-slate-700"
    >
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>
  )
}
