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

  if (rows.length === 0) {
    return null
  }

  const columns = Object.keys(rows[0])
  if (!columns.includes(x)) {
    return <p className="text-sm text-amber-600">Column '{x}' not found.</p>
  }
  if (!columns.includes(y)) {
    return <p className="text-sm text-amber-600">Column '{y}' not found.</p>
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
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              {horizontal ? (
                <>
                  <XAxis type="number" tick={{ fontSize: 12 }} />
                  <YAxis
                    type="category"
                    dataKey={x}
                    width={120}
                    tick={{ fontSize: 12 }}
                  />
                </>
              ) : (
                <>
                  <XAxis dataKey={x} tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                </>
              )}
              <Tooltip />
              <Bar dataKey={y} fill={CHART_COLORS[0]} radius={4} />
            </BarChart>
          </ResponsiveContainer>
        )
      }

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <LineChart data={sortedRows} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey={x} tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
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
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )
      }

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <ScatterChart margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey={x} type="number" name={x} tick={{ fontSize: 12 }} />
              <YAxis dataKey={y} type="number" name={y} tick={{ fontSize: 12 }} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter data={sortedRows} fill={CHART_COLORS[0]} />
            </ScatterChart>
          </ResponsiveContainer>
        )

      case 'grouped_bar':
      case 'stacked_bar': {
        if (!color) {
          return <p className="text-sm text-amber-600">Missing grouping column.</p>
        }
        const { data, seriesKeys } = pivotByColor(rows, x, y, color)
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <BarChart data={data} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey={x} tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
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
              stroke="#fff"
              fill={CHART_COLORS[0]}
            >
              <Tooltip />
            </Treemap>
          </ResponsiveContainer>
        )
      }

      case 'heatmap': {
        if (!color) {
          return <p className="text-sm text-amber-600">Missing grouping column.</p>
        }
        const heatmap = buildHeatmapMatrix(rows, x, y, color)
        return <HeatmapGrid heatmap={heatmap} />
      }

      default:
        return (
          <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
            <BarChart data={sortedRows} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey={x} tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
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
        className="rounded-md border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50"
        onClick={() => downloadCsv(rows)}
      >
        📥 Download Results
      </button>
    </div>
  )
}
