import type { ChartInfo, DashboardWidget, ResultRow } from '../api/types'

export interface UserChatMessage {
  role: 'user'
  content: string
}

export interface AssistantChatMessage {
  role: 'assistant'
  content: string
  sql?: string
  result?: ResultRow[]
  chart?: ChartInfo | null
}

export interface DashboardChatMessage {
  role: 'dashboard'
  dashboardType?: string
  widgets: DashboardWidget[]
}

export type ChatMessage =
  | UserChatMessage
  | AssistantChatMessage
  | DashboardChatMessage
