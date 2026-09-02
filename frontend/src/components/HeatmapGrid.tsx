import { useIsDarkMode } from '../hooks/useIsDarkMode'
import type { HeatmapMatrix } from '../lib/chartData'

interface HeatmapGridProps {
  heatmap: HeatmapMatrix
}

function cellBackground(value: number, maxValue: number, isDark: boolean): string {
  const base = isDark ? '129, 140, 248' : '99, 102, 241'
  if (maxValue <= 0) return `rgba(${base}, 0.08)`
  const intensity = 0.12 + 0.75 * (value / maxValue)
  return `rgba(${base}, ${intensity.toFixed(2)})`
}

export function HeatmapGrid({ heatmap }: HeatmapGridProps) {
  const { xValues, colorValues, matrix, maxValue } = heatmap
  const isDark = useIsDarkMode()

  return (
    <div className="overflow-auto rounded-md border border-slate-200 dark:border-slate-700">
      <table className="min-w-full border-collapse text-xs">
        <thead>
          <tr>
            <th className="sticky left-0 bg-slate-50 px-3 py-2 text-left font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">
              &nbsp;
            </th>
            {colorValues.map((column) => (
              <th
                key={column}
                className="whitespace-nowrap bg-slate-50 px-3 py-2 text-left font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {xValues.map((row) => (
            <tr key={row}>
              <td className="sticky left-0 whitespace-nowrap bg-slate-50 px-3 py-2 font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                {row}
              </td>
              {colorValues.map((column) => {
                const value = matrix[row]?.[column] ?? 0
                return (
                  <td
                    key={column}
                    className="whitespace-nowrap px-3 py-2 text-center text-slate-800 dark:text-slate-100"
                    style={{ backgroundColor: cellBackground(value, maxValue, isDark) }}
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
