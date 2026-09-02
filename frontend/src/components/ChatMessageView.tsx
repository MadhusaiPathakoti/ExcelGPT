import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import type { ChatMessage } from '../types/chat'
import { ChartRenderer } from './ChartRenderer'
import { DataTable } from './DataTable'

interface ChatMessageViewProps {
  message: ChatMessage
  onRegenerate?: (editedQuestion: string) => void
  isRegenerating?: boolean
}

export function ChatMessageView({
  message,
  onRegenerate,
  isRegenerating,
}: ChatMessageViewProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [draft, setDraft] = useState(
    message.role === 'user' ? message.content : '',
  )

  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-2xl rounded-2xl bg-indigo-600 px-4 py-2.5 text-sm text-white">
          {isEditing ? (
            <div className="space-y-2">
              <textarea
                className="w-full min-w-[16rem] rounded-md border border-indigo-300 bg-white px-2 py-1.5 text-sm text-slate-900 dark:border-indigo-700 dark:bg-slate-900 dark:text-slate-100"
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                rows={3}
              />
              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  className="rounded-md bg-indigo-500 px-3 py-1 text-xs font-medium hover:bg-indigo-400"
                  disabled={isRegenerating}
                  onClick={() => {
                    onRegenerate?.(draft)
                    setIsEditing(false)
                  }}
                >
                  {isRegenerating ? 'Regenerating...' : '🔄 Regenerate'}
                </button>
                <button
                  type="button"
                  className="rounded-md bg-indigo-700 px-3 py-1 text-xs font-medium hover:bg-indigo-800"
                  onClick={() => {
                    setDraft(message.content)
                    setIsEditing(false)
                  }}
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-start gap-2">
              <p className="whitespace-pre-wrap">{message.content}</p>
              <button
                type="button"
                title="Edit question"
                className="shrink-0 text-xs text-indigo-200 hover:text-white"
                onClick={() => {
                  setDraft(message.content)
                  setIsEditing(true)
                }}
              >
                ✏️
              </button>
            </div>
          )}
        </div>
      </div>
    )
  }

  if (message.role === 'dashboard') {
    return (
      <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800">
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          📊 AI Dashboard{' '}
          {message.dashboardType ? `— ${message.dashboardType}` : ''}
        </h3>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {message.widgets.map((widget, index) => (
            <div
              key={index}
              className="rounded-md border border-slate-200 p-3 dark:border-slate-700"
            >
              <p className="mb-2 text-sm font-medium text-slate-800 dark:text-slate-200">
                {widget.title}
              </p>
              {widget.error ? (
                <p className="text-sm text-red-600 dark:text-red-400">
                  {widget.error}
                </p>
              ) : (
                <div className="space-y-3">
                  {widget.result && widget.result.length > 0 && (
                    <DataTable rows={widget.result} maxHeight="12rem" />
                  )}
                  {widget.chart && widget.result && (
                    <ChartRenderer chart={widget.chart} rows={widget.result} />
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-3xl space-y-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-800 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
        <div className="leading-relaxed [&_a]:text-indigo-600 [&_code]:rounded [&_code]:bg-slate-100 [&_code]:px-1 [&_p]:my-1 [&_ul]:my-1 [&_ul]:list-disc [&_ul]:pl-5 dark:[&_a]:text-indigo-400 dark:[&_code]:bg-slate-700">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {message.sql && (
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Generated SQL
            </p>
            <pre className="overflow-auto rounded-md bg-slate-900 px-3 py-2 text-xs text-slate-100 dark:bg-slate-950">
              <code>{message.sql}</code>
            </pre>
          </div>
        )}

        {message.result && message.result.length > 0 && (
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Results
            </p>
            <DataTable rows={message.result} />
          </div>
        )}

        {message.chart && message.result && (
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Visualization
            </p>
            <ChartRenderer chart={message.chart} rows={message.result} />
          </div>
        )}
      </div>
    </div>
  )
}
