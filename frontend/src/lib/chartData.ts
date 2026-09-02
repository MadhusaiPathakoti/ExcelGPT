import type { ResultRow } from '../api/types'

export const CHART_COLORS = [
  '#6366f1',
  '#22c55e',
  '#f59e0b',
  '#ef4444',
  '#06b6d4',
  '#a855f7',
  '#ec4899',
  '#84cc16',
]

export function isNumericColumn(rows: ResultRow[], key: string): boolean {
  return rows.every((row) => {
    const value = row[key]
    return value === null || value === undefined || typeof value === 'number'
  })
}

export function numericValue(value: unknown): number {
  if (typeof value === 'number') return value
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : 0
}

export function sortByKeyDescending(rows: ResultRow[], key: string): ResultRow[] {
  return [...rows].sort((a, b) => numericValue(b[key]) - numericValue(a[key]))
}

export function toCsv(rows: ResultRow[]): string {
  if (rows.length === 0) return ''
  const columns = Object.keys(rows[0])

  function escapeCell(value: unknown): string {
    const text = value === null || value === undefined ? '' : String(value)
    if (/[",\n]/.test(text)) {
      return `"${text.replace(/"/g, '""')}"`
    }
    return text
  }

  const lines = [columns.map(escapeCell).join(',')]
  for (const row of rows) {
    lines.push(columns.map((column) => escapeCell(row[column])).join(','))
  }
  return lines.join('\n')
}

export function downloadCsv(rows: ResultRow[], filename = 'results.csv') {
  const csv = toCsv(rows)
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

export interface PivotedSeries {
  data: Record<string, string | number>[]
  seriesKeys: string[]
}

export function pivotByColor(
  rows: ResultRow[],
  xKey: string,
  yKey: string,
  colorKey: string,
): PivotedSeries {
  const seriesKeysSet = new Set<string>()
  const byX = new Map<string, Record<string, string | number>>()

  for (const row of rows) {
    const xValue = String(row[xKey] ?? '')
    const colorValue = String(row[colorKey] ?? '')
    seriesKeysSet.add(colorValue)

    if (!byX.has(xValue)) {
      byX.set(xValue, { [xKey]: xValue })
    }
    byX.get(xValue)![colorValue] = numericValue(row[yKey])
  }

  return {
    data: Array.from(byX.values()),
    seriesKeys: Array.from(seriesKeysSet),
  }
}

export interface TreemapNode {
  name: string
  size?: number
  children?: TreemapNode[]
  [key: string]: unknown
}

export function buildTreemapData(
  rows: ResultRow[],
  xKey: string,
  yKey: string,
  colorKey?: string,
): TreemapNode[] {
  if (!colorKey) {
    return rows.map((row) => ({
      name: String(row[xKey] ?? ''),
      size: numericValue(row[yKey]),
    }))
  }

  const byX = new Map<string, TreemapNode>()
  for (const row of rows) {
    const xValue = String(row[xKey] ?? '')
    if (!byX.has(xValue)) {
      byX.set(xValue, { name: xValue, children: [] })
    }
    byX.get(xValue)!.children!.push({
      name: String(row[colorKey] ?? ''),
      size: numericValue(row[yKey]),
    })
  }
  return Array.from(byX.values())
}

export interface HeatmapMatrix {
  xValues: string[]
  colorValues: string[]
  matrix: Record<string, Record<string, number>>
  maxValue: number
}

export function buildHeatmapMatrix(
  rows: ResultRow[],
  xKey: string,
  yKey: string,
  colorKey: string,
): HeatmapMatrix {
  const xValues: string[] = []
  const colorValues: string[] = []
  const matrix: Record<string, Record<string, number>> = {}
  let maxValue = 0

  for (const row of rows) {
    const xValue = String(row[xKey] ?? '')
    const colorValue = String(row[colorKey] ?? '')
    const value = numericValue(row[yKey])

    if (!xValues.includes(xValue)) xValues.push(xValue)
    if (!colorValues.includes(colorValue)) colorValues.push(colorValue)

    matrix[xValue] ??= {}
    matrix[xValue][colorValue] = (matrix[xValue][colorValue] ?? 0) + value
    maxValue = Math.max(maxValue, matrix[xValue][colorValue])
  }

  return { xValues, colorValues, matrix, maxValue }
}
