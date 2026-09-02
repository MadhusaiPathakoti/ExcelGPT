import type { ResultRow } from '../api/types'

interface DataTableProps {
  rows: ResultRow[]
  maxHeight?: string
}

export function DataTable({ rows, maxHeight = '20rem' }: DataTableProps) {
  if (!rows || rows.length === 0) {
    return (
      <p className="text-sm text-slate-500 dark:text-slate-400">
        No data available.
      </p>
    )
  }

  const columns = Object.keys(rows[0])

  return (
    <div
      className="overflow-auto rounded-md border border-slate-200 dark:border-slate-700"
      style={{ maxHeight }}
    >
      <table className="min-w-full divide-y divide-slate-200 text-sm dark:divide-slate-700">
        <thead className="sticky top-0 bg-slate-50 dark:bg-slate-800">
          <tr>
            {columns.map((column) => (
              <th
                key={column}
                className="whitespace-nowrap px-3 py-2 text-left font-medium text-slate-600 dark:text-slate-300"
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 bg-white dark:divide-slate-800 dark:bg-slate-900">
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td
                  key={column}
                  className="whitespace-nowrap px-3 py-2 text-slate-700 dark:text-slate-300"
                >
                  {row[column] === null || row[column] === undefined
                    ? ''
                    : String(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
