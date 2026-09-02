import { useRef, useState } from 'react'
import { sendVoice } from '../api/client'

interface VoiceRecorderProps {
  onTranscribed: (question: string) => void
  disabled?: boolean
}

type RecordingState = 'idle' | 'recording' | 'processing'

export function VoiceRecorder({ onTranscribed, disabled }: VoiceRecorderProps) {
  const [state, setState] = useState<RecordingState>('idle')
  const [error, setError] = useState<string | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const streamRef = useRef<MediaStream | null>(null)

  async function handleStop() {
    const blob = new Blob(chunksRef.current, { type: 'audio/webm' })

    try {
      const response = await sendVoice(blob)
      const question = response.question?.trim()
      if (question) {
        onTranscribed(question)
      } else {
        setError('No speech recognized.')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Voice transcription failed.')
    } finally {
      setState('idle')
    }
  }

  async function startRecording() {
    setError(null)

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream
      chunksRef.current = []

      const recorder = new MediaRecorder(stream)
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data)
      }
      recorder.onstop = handleStop

      mediaRecorderRef.current = recorder
      recorder.start()
      setState('recording')
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Microphone unavailable.',
      )
      setState('idle')
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop()
    streamRef.current?.getTracks().forEach((track) => track.stop())
    setState('processing')
  }

  return (
    <div className="flex shrink-0 items-center gap-2">
      {state === 'idle' && (
        <button
          type="button"
          onClick={startRecording}
          disabled={disabled}
          className="whitespace-nowrap rounded-md border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50 disabled:opacity-50 dark:border-slate-600 dark:bg-slate-800 dark:hover:bg-slate-700"
        >
          🎤 Voice
        </button>
      )}

      {state === 'recording' && (
        <button
          type="button"
          onClick={stopRecording}
          className="flex items-center gap-1.5 whitespace-nowrap rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-800 dark:bg-red-950/40 dark:text-red-300"
        >
          <span className="h-2 w-2 shrink-0 animate-pulse rounded-full bg-red-500" />
          ⏹ Stop
        </button>
      )}

      {state === 'processing' && (
        <span className="whitespace-nowrap rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400">
          Transcribing...
        </span>
      )}

      {error && (
        <span className="text-xs text-red-600 dark:text-red-400">{error}</span>
      )}
    </div>
  )
}
