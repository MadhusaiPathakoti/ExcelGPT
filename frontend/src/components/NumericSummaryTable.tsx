interface NumericSummaryTableProps {
  summary: Record<string, Record<string, unknown>>
}

function formatValue(value: unknown): string {
  if (typeof value === 'number') return value.toLocaleString(undefined, { maximumFractionDigits: 2 })
  if (value === '' || value === null || value === undefined) return ''
  return String(value)
}

export function NumericSummaryTable({ summary }: NumericSummaryTableProps) {
  const columns = Object.keys(summary)

  if (columns.length === 0) {
    return <p className="text-sm text-slate-500">No numeric columns detected.</p>
  }

  const statNames = Object.keys(summary[columns[0]])

  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-3 py-2 text-left font-medium text-slate-600">Statistic</th>
            {columns.map((column) => (
              <th key={column} className="whitespace-nowrap px-3 py-2 text-left font-medium text-slate-600">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 bg-white">
          {statNames.map((stat) => (
            <tr key={stat}>
              <td className="px-3 py-2 font-medium text-slate-600">{stat}</td>
              {columns.map((column) => (
                <td key={column} className="whitespace-nowrap px-3 py-2 text-slate-700">
                  {formatValue(summary[column]?.[stat])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
