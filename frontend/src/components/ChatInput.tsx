import { useState } from 'react'
import type { FormEvent } from 'react'

interface ChatInputProps {
  onSubmit: (question: string) => void
  disabled?: boolean
}

export function ChatInput({ onSubmit, disabled }: ChatInputProps) {
  const [value, setValue] = useState('')

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSubmit(trimmed)
    setValue('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Ask a question about your data..."
        className="flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-indigo-400 focus:outline-none"
        disabled={disabled}
      />
      <button
        type="submit"
        className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        disabled={disabled || !value.trim()}
      >
        Send
      </button>
    </form>
  )
}
