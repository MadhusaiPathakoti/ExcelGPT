export interface TableInfo {
  table_name: string
  rows: number
  columns: number
}

export interface Relationship {
  left_table: string
  left_column: string
  right_table: string
  right_column: string
  relationship?: string
}

export type ChartType =
  | 'bar'
  | 'line'
  | 'pie'
  | 'scatter'
  | 'grouped_bar'
  | 'stacked_bar'
  | 'treemap'
  | 'heatmap'

export interface ChartInfo {
  chart_type: ChartType
  x: string
  y: string
  color?: string
}

export type ResultRow = Record<string, string | number | null>

export interface DatasetProfile {
  rows?: number
  columns?: number
  missing_values?: Record<string, number>
  duplicates?: number
  numeric_summary?: Record<string, unknown>
  categorical_summary?: Record<string, unknown>
  [key: string]: unknown
}

export interface DatasetInsights {
  top_product?: string
  best_region?: string
  most_ordered_product?: string
  total_revenue?: number
  missing_cells?: number
  outliers?: number
  summary?: string[]
  [key: string]: unknown
}

export interface UploadResult {
  session_id: string
  tables: TableInfo[]
  relationships: Relationship[]
  profile: DatasetProfile
  quality_score: number
  suggested_questions: string[]
  insights: DatasetInsights
  previews: Record<string, ResultRow[]>
}

export interface ChatAnswer {
  answer: string
  sql: string
  result: ResultRow[]
  chart: ChartInfo | null
  intent?: string
  tables?: TableInfo[]
  relationships?: Relationship[]
}

export interface DashboardWidget {
  title: string
  question?: string
  sql?: string
  result?: ResultRow[]
  chart?: ChartInfo | null
  error?: string
}

export interface DashboardAnswer {
  intent: 'dashboard'
  dashboard_type?: string
  widgets: DashboardWidget[]
}

export type ChatResponse = ChatAnswer | DashboardAnswer

export function isDashboardResponse(
  response: ChatResponse,
): response is DashboardAnswer {
  return response.intent === 'dashboard'
}

export interface VoiceResponse {
  question: string
}
