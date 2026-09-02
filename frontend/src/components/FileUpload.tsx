import { useRef, useState } from 'react'
import type { DragEvent } from 'react'
import { uploadFiles } from '../api/client'
import type { UploadResult } from '../api/types'

interface FileUploadProps {
  onUploaded: (result: UploadResult) => void
}

const ACCEPTED_EXTENSIONS = ['.xlsx', '.xls']

function isAcceptedFile(file: File): boolean {
  const name = file.name.toLowerCase()
  return ACCEPTED_EXTENSIONS.some((ext) => name.endsWith(ext))
}

export function FileUpload({ onUploaded }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  async function handleFiles(fileList: FileList | null) {
    if (!fileList || fileList.length === 0) return

    const files = Array.from(fileList).filter(isAcceptedFile)

    if (files.length === 0) {
      setError('Please select .xlsx or .xls files.')
      return
    }

    setError(null)
    setIsUploading(true)

    try {
      const result = await uploadFiles(files)
      onUploaded(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed.')
    } finally {
      setIsUploading(false)
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    setIsDragging(false)
    handleFiles(event.dataTransfer.files)
  }

  return (
    <div>
      <div
        className={
          'flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 text-center transition-colors ' +
          (isDragging
            ? 'border-indigo-400 bg-indigo-50'
            : 'border-slate-300 bg-white hover:border-slate-400')
        }
        onDragOver={(event) => {
          event.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        {isUploading ? (
          <>
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
            <p className="mt-4 text-sm font-medium text-slate-600">
              Analyzing dataset...
            </p>
          </>
        ) : (
          <>
            <p className="text-sm font-medium text-slate-700">
              Drag and drop Excel files here
            </p>
            <p className="mt-1 text-xs text-slate-500">
              or click below to browse (.xlsx, .xls, multiple files supported)
            </p>
            <button
              type="button"
              className="mt-4 rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
              onClick={() => inputRef.current?.click()}
            >
              Upload Excel Files
            </button>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          multiple
          accept=".xlsx,.xls"
          className="hidden"
          onChange={(event) => handleFiles(event.target.files)}
        />
      </div>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
    </div>
  )
}
