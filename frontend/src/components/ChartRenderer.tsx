import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  Treemap,
  XAxis,
  YAxis,
} from 'recharts'
import type { ChartInfo, ResultRow } from '../api/types'
import { useIsDarkMode } from '../hooks/useIsDarkMode'
import {
  CHART_COLORS,
  buildHeatmapMatrix,
  buildTreemapData,
  downloadCsv,
  isNumericColumn,
  pivotByColor,
  sortByKeyDescending,
} from '../lib/chartData'
import { HeatmapGrid } from './HeatmapGrid'
import { KpiRow } from './KpiRow'

interface ChartRendererProps {
  chart: ChartInfo
  rows: ResultRow[]
}

const CHART_HEIGHT = 340

export function ChartRenderer({ chart, rows }: ChartRendererProps) {
  const { chart_type: chartType, x, y, color } = chart
  const isDark = useIsDarkMode()
  const gridStroke = isDark ? '#334155' : '#e2e8f0'
  const tickStyle = { fontSize: 12, fill: isDark ? '#94a3b8' : '#475569' }
  const tooltipStyle = {
    contentStyle: {
      backgroundColor: isDark ? '#1e293b' : '#ffffff',
      border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
      color: isDark ? '#e2e8f0' : '#0f172a',
      fontSize: 12,
      borderRadius: 6,
    },
    labelStyle: { color: isDark ? '#e2e8f0' : '#0f172a' },
  }
  const legendStyle = { color: isDark ? '#cbd5e1' : '#475569', fontSize: 12 }

  if (rows.length === 0) {
    return null
  }

  const columns = Object.keys(rows[0])
  if (!columns.includes(x)) {
    return (
      <p className="text-sm text-amber-600 dark:text-amber-400">
        Column '{x}' not found.
      </p>
    )
  }
  if (!columns.includes(y)) {
    return (
      <p className="text-sm text-amber-600 dark:text-amber-400">
        Column '{y}' not found.
      </p>
    )
  }

  const yIsNumeric = isNumericColumn(rows, y)
  const sortedRows =
    chartType === 'line' || chartType === 'grouped_bar'
      ? rows
      : sortByKeyDescending(rows, y)

  function renderChart() {
    switch (chartType) {
      case 'bar': {
        const horizontal = sortedRows.length >= 6
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <BarChart
              data={sortedRows}
              layout={horizontal ? 'vertical' : 'horizontal'}
              margin={{ top: 8, right: 16, left: 8, bottom: 8 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              {horizontal ? (
                <>
                  <XAxis type="number" tick={tickStyle} />
                  <YAxis
                    type="category"
                    dataKey={x}
                    width={120}
                    tick={tickStyle}
                  />
                </>
              ) : (
                <>
                  <XAxis dataKey={x} tick={tickStyle} />
                  <YAxis tick={tickStyle} />
                </>
              )}
              <Tooltip {...tooltipStyle} />
              <Bar dataKey={y} fill={CHART_COLORS[0]} radius={4} />
            </BarChart>
          </ResponsiveContainer>
        )
      }

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <LineChart data={sortedRows} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              <XAxis dataKey={x} tick={tickStyle} />
              <YAxis tick={tickStyle} />
              <Tooltip {...tooltipStyle} />
              <Line
                type="monotone"
                dataKey={y}
                stroke={CHART_COLORS[0]}
                strokeWidth={3}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )

      case 'pie': {
        const pieData = sortedRows.slice(0, 10)
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey={y}
                nameKey={x}
                innerRadius={60}
                outerRadius={110}
                label={(entry) =>
                  `${(entry as unknown as ResultRow)[x]} (${(
                    (entry.percent ?? 0) * 100
                  ).toFixed(0)}%)`
                }
              >
                {pieData.map((_, index) => (
                  <Cell key={index} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip {...tooltipStyle} />
              <Legend wrapperStyle={legendStyle} />
            </PieChart>
          </ResponsiveContainer>
        )
      }

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <ScatterChart margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              <XAxis dataKey={x} type="number" name={x} tick={tickStyle} />
              <YAxis dataKey={y} type="number" name={y} tick={tickStyle} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} {...tooltipStyle} />
              <Scatter data={sortedRows} fill={CHART_COLORS[0]} />
            </ScatterChart>
          </ResponsiveContainer>
        )

      case 'grouped_bar':
      case 'stacked_bar': {
        if (!color) {
          return (
            <p className="text-sm text-amber-600 dark:text-amber-400">
              Missing grouping column.
            </p>
          )
        }
        const { data, seriesKeys } = pivotByColor(rows, x, y, color)
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <BarChart data={data} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              <XAxis dataKey={x} tick={tickStyle} />
              <YAxis tick={tickStyle} />
              <Tooltip {...tooltipStyle} />
              <Legend wrapperStyle={legendStyle} />
              {seriesKeys.map((key, index) => (
                <Bar
                  key={key}
                  dataKey={key}
                  fill={CHART_COLORS[index % CHART_COLORS.length]}
                  stackId={chartType === 'stacked_bar' ? 'stack' : undefined}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        )
      }

      case 'treemap': {
        const data = buildTreemapData(rows, x, y, color)
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <Treemap
              data={data}
              dataKey="size"
              nameKey="name"
              stroke={isDark ? '#1e293b' : '#fff'}
              fill={CHART_COLORS[0]}
            >
              <Tooltip {...tooltipStyle} />
            </Treemap>
          </ResponsiveContainer>
        )
      }

      case 'heatmap': {
        if (!color) {
          return (
            <p className="text-sm text-amber-600 dark:text-amber-400">
              Missing grouping column.
            </p>
          )
        }
        const heatmap = buildHeatmapMatrix(rows, x, y, color)
        return <HeatmapGrid heatmap={heatmap} />
      }

      default:
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <BarChart data={sortedRows} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              <XAxis dataKey={x} tick={tickStyle} />
              <YAxis tick={tickStyle} />
              <Tooltip {...tooltipStyle} />
              <Bar dataKey={y} fill={CHART_COLORS[0]} radius={4} />
            </BarChart>
          </ResponsiveContainer>
        )
    }
  }

  return (
    <div className="space-y-3">
      {yIsNumeric && <KpiRow rows={rows} yKey={y} />}
      {renderChart()}
      <button
        type="button"
        className="rounded-md border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
        onClick={() => downloadCsv(rows)}
      >
        📥 Download Results
      </button>
    </div>
  )
}
