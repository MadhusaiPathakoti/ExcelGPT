import type { HeatmapMatrix } from '../lib/chartData'

interface HeatmapGridProps {
  heatmap: HeatmapMatrix
}

function cellBackground(value: number, maxValue: number): string {
  if (maxValue <= 0) return 'rgba(99, 102, 241, 0.05)'
  const intensity = 0.1 + 0.8 * (value / maxValue)
  return `rgba(99, 102, 241, ${intensity.toFixed(2)})`
}

export function HeatmapGrid({ heatmap }: HeatmapGridProps) {
  const { xValues, colorValues, matrix, maxValue } = heatmap

  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="min-w-full border-collapse text-xs">
        <thead>
          <tr>
            <th className="sticky left-0 bg-slate-50 px-3 py-2 text-left font-medium text-slate-600">
              &nbsp;
            </th>
            {colorValues.map((column) => (
              <th
                key={column}
                className="whitespace-nowrap bg-slate-50 px-3 py-2 text-left font-medium text-slate-600"
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {xValues.map((row) => (
            <tr key={row}>
              <td className="sticky left-0 whitespace-nowrap bg-slate-50 px-3 py-2 font-medium text-slate-600">
                {row}
              </td>
              {colorValues.map((column) => {
                const value = matrix[row]?.[column] ?? 0
                return (
                  <td
                    key={column}
                    className="whitespace-nowrap px-3 py-2 text-center text-slate-800"
                    style={{ backgroundColor: cellBackground(value, maxValue) }}
                  >
                    {value.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
