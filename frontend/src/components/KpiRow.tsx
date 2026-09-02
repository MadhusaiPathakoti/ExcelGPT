import { numericValue } from '../lib/chartData'
import type { ResultRow } from '../api/types'
import { StatCard } from './StatCard'

interface KpiRowProps {
  rows: ResultRow[]
  yKey: string
}

function formatNumber(value: number): string {
  return Number.isInteger(value)
    ? value.toLocaleString()
    : value.toLocaleString(undefined, { maximumFractionDigits: 2 })
}

export function KpiRow({ rows, yKey }: KpiRowProps) {
  const values = rows.map((row) => numericValue(row[yKey]))
  if (values.length === 0) return null

  const total = values.reduce((sum, value) => sum + value, 0)
  const average = total / values.length
  const max = Math.max(...values)

  return (
    <div className="grid grid-cols-3 gap-3">
      <StatCard label="Total" value={formatNumber(Math.round(total * 100) / 100)} />
      <StatCard label="Average" value={formatNumber(Math.round(average * 100) / 100)} />
      <StatCard label="Maximum" value={formatNumber(Math.round(max * 100) / 100)} />
    </div>
  )
}
