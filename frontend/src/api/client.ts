import type { ChatResponse, UploadResult, VoiceResponse } from './types'

export const API_BASE_URL: string =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

const ROOT_URL = API_BASE_URL.replace(/\/api\/?$/, '') || '/'

class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function parseJsonOrThrow<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }
  return (await response.json()) as T
}

export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(ROOT_URL)
  return parseJsonOrThrow(response)
}

export async function uploadFiles(files: File[]): Promise<UploadResult> {
  const formData = new FormData()
  for (const file of files) {
    formData.append('files', file)
  }

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  })

  return parseJsonOrThrow(response)
}

export async function sendChat(
  sessionId: string,
  question: string,
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, question }),
  })

  return parseJsonOrThrow(response)
}

export async function sendVoice(audioBlob: Blob): Promise<VoiceResponse> {
  const formData = new FormData()
  formData.append('file', audioBlob, 'voice.webm')

  const response = await fetch(`${API_BASE_URL}/voice`, {
    method: 'POST',
    body: formData,
  })

  return parseJsonOrThrow(response)
}
