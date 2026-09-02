import type { ReactNode } from 'react'

interface CollapsibleSectionProps {
  title: string
  defaultOpen?: boolean
  children: ReactNode
}

export function CollapsibleSection({
  title,
  defaultOpen = false,
  children,
}: CollapsibleSectionProps) {
  return (
    <details
      className="group rounded-lg border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800"
      open={defaultOpen}
    >
      <summary className="flex cursor-pointer list-none items-center justify-between px-4 py-3 text-sm font-medium text-slate-800 dark:text-slate-200">
        {title}
        <span className="text-slate-400 transition-transform group-open:rotate-90 dark:text-slate-500">
          ▶
        </span>
      </summary>
      <div className="border-t border-slate-100 px-4 py-3 dark:border-slate-700">
        {children}
      </div>
    </details>
  )
}
