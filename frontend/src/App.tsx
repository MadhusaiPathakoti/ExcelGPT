import { useEffect, useState } from 'react'
import { checkHealth } from './api/client'
import type { UploadResult } from './api/types'
import { Chat } from './components/Chat'
import { DatasetOverview } from './components/DatasetOverview'
import { FileUpload } from './components/FileUpload'

type BackendStatus = 'checking' | 'online' | 'offline'

function App() {
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('checking')
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)

  useEffect(() => {
    let cancelled = false

    checkHealth()
      .then(() => {
        if (!cancelled) setBackendStatus('online')
      })
      .catch(() => {
        if (!cancelled) setBackendStatus('offline')
      })

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 px-6 py-4">
          <div>
            <h1 className="text-xl font-semibold text-slate-900">ExcelGPT</h1>
            <p className="text-sm text-slate-500">
              AI-powered business intelligence assistant
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            {uploadResult && (
              <button
                type="button"
                className="rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-100"
                onClick={() => setUploadResult(null)}
              >
                Upload different files
              </button>
            )}
            <span
              className={
                'flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium ' +
                (backendStatus === 'online'
                  ? 'bg-emerald-100 text-emerald-700'
                  : backendStatus === 'offline'
                    ? 'bg-red-100 text-red-700'
                    : 'bg-slate-100 text-slate-500')
              }
            >
              <span
                className={
                  'h-2 w-2 rounded-full ' +
                  (backendStatus === 'online'
                    ? 'bg-emerald-500'
                    : backendStatus === 'offline'
                      ? 'bg-red-500'
                      : 'bg-slate-400')
                }
              />
              {backendStatus === 'online'
                ? 'Backend connected'
                : backendStatus === 'offline'
                  ? 'Backend unreachable'
                  : 'Checking backend...'}
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-10">
        {!uploadResult ? (
          <FileUpload onUploaded={setUploadResult} />
        ) : (
          <>
            <DatasetOverview result={uploadResult} />
            <Chat
              sessionId={uploadResult.session_id}
              suggestedQuestions={uploadResult.suggested_questions}
            />
          </>
        )}
      </main>
    </div>
  )
}

export default App
