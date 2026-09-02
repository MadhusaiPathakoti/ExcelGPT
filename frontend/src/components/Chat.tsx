import { useEffect, useRef, useState } from 'react'
import { sendChat } from '../api/client'
import { isDashboardResponse } from '../api/types'
import type { ChatMessage } from '../types/chat'
import { ChatInput } from './ChatInput'
import { ChatMessageView } from './ChatMessageView'
import { VoiceRecorder } from './VoiceRecorder'

interface ChatProps {
  sessionId: string
  suggestedQuestions?: string[]
}

function responseToMessage(response: Awaited<ReturnType<typeof sendChat>>): ChatMessage {
  if (isDashboardResponse(response)) {
    return {
      role: 'dashboard',
      dashboardType: response.dashboard_type,
      widgets: response.widgets,
    }
  }

  return {
    role: 'assistant',
    content: response.answer || 'No response generated.',
    sql: response.sql,
    result: response.result,
    chart: response.chart,
  }
}

export function Chat({ sessionId, suggestedQuestions = [] }: ChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [regeneratingIndex, setRegeneratingIndex] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages.length])

  async function askQuestion(question: string) {
    setError(null)
    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setIsLoading(true)

    try {
      const response = await sendChat(sessionId, question)
      setMessages((prev) => [...prev, responseToMessage(response)])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get a response.')
    } finally {
      setIsLoading(false)
    }
  }

  async function regenerateAt(index: number, editedQuestion: string) {
    setError(null)
    setRegeneratingIndex(index)

    try {
      const response = await sendChat(sessionId, editedQuestion)
      setMessages((prev) => [
        ...prev.slice(0, index),
        { role: 'user', content: editedQuestion },
        responseToMessage(response),
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to regenerate.')
    } finally {
      setRegeneratingIndex(null)
    }
  }

  return (
    <section className="mt-8">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
        💬 Chat With Your Data
      </h2>

      {messages.length === 0 && suggestedQuestions.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2">
          {suggestedQuestions.map((question, index) => (
            <button
              key={index}
              type="button"
              className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs text-slate-600 hover:border-indigo-300 hover:text-indigo-600"
              onClick={() => askQuestion(question)}
            >
              {question}
            </button>
          ))}
        </div>
      )}

      <div className="space-y-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
        {messages.length === 0 && (
          <p className="text-center text-sm text-slate-400">
            Ask a question to get started.
          </p>
        )}

        {messages.map((message, index) => (
          <ChatMessageView
            key={index}
            message={message}
            isRegenerating={regeneratingIndex === index}
            onRegenerate={
              message.role === 'user'
                ? (editedQuestion) => regenerateAt(index, editedQuestion)
                : undefined
            }
          />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-500">
              <span className="h-2 w-2 animate-pulse rounded-full bg-indigo-400" />
              Thinking...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}

      <div className="mt-3 flex items-start gap-2">
        <VoiceRecorder onTranscribed={askQuestion} disabled={isLoading} />
        <div className="flex-1">
          <ChatInput onSubmit={askQuestion} disabled={isLoading} />
        </div>
      </div>
    </section>
  )
}
