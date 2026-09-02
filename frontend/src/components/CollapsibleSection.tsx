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
      className="group rounded-lg border border-slate-200 bg-white"
      open={defaultOpen}
    >
      <summary className="flex cursor-pointer list-none items-center justify-between px-4 py-3 text-sm font-medium text-slate-800">
        {title}
        <span className="text-slate-400 transition-transform group-open:rotate-90">
          ▶
        </span>
      </summary>
      <div className="border-t border-slate-100 px-4 py-3">{children}</div>
    </details>
  )
}
