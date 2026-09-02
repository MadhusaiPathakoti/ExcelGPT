import { CollapsibleSection } from './CollapsibleSection'
import { DataTable } from './DataTable'
import { NumericSummaryTable } from './NumericSummaryTable'
import { StatCard } from './StatCard'
import type { UploadResult } from '../api/types'

interface DatasetOverviewProps {
  result: UploadResult
}

function titleCase(key: string): string {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
}

export function DatasetOverview({ result }: DatasetOverviewProps) {
  const { profile, insights, tables, relationships, previews, suggested_questions } = result

  const categoricalSummary = (profile.categorical_summary ?? {}) as Record<
    string,
    { unique_values: number; top_value: string | null }
  >
  const missingValues = (profile.missing_values ?? {}) as Record<string, number>
  const numericSummary = (profile.numeric_summary ?? {}) as Record<
    string,
    Record<string, unknown>
  >

  const insightEntries = Object.entries(insights).filter(
    ([key]) => key !== 'error' && key !== 'summary',
  )
  const totalRows = tables.reduce((sum, table) => sum + table.rows, 0)

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-800 dark:border-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300">
        Dataset uploaded successfully
      </div>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400 dark:text-slate-400">
          Dataset Overview
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <StatCard label="Rows" value={profile.rows ?? 0} />
          <StatCard label="Columns" value={profile.columns ?? 0} />
          <StatCard label="Quality Score" value={result.quality_score} />
        </div>
      </section>

      <section className="space-y-3">
        <CollapsibleSection title="Missing Values">
          {Object.keys(missingValues).length === 0 ? (
            <p className="text-sm text-slate-500 dark:text-slate-400">
              No missing value data.
            </p>
          ) : (
            <ul className="space-y-1 text-sm text-slate-700 dark:text-slate-300">
              {Object.entries(missingValues).map(([column, count]) => (
                <li key={column} className="flex justify-between">
                  <span>{column}</span>
                  <span className="font-medium">{count}</span>
                </li>
              ))}
            </ul>
          )}
        </CollapsibleSection>

        <CollapsibleSection title="Duplicate Rows">
          <p className="text-sm text-slate-700 dark:text-slate-300">
            {profile.duplicates ?? 0}
          </p>
        </CollapsibleSection>

        {Object.keys(numericSummary).length > 0 && (
          <CollapsibleSection title="Numeric Statistics">
            <NumericSummaryTable summary={numericSummary} />
          </CollapsibleSection>
        )}

        {Object.keys(categoricalSummary).length > 0 && (
          <CollapsibleSection title="Categorical Summary">
            <ul className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
              {Object.entries(categoricalSummary).map(([column, stats]) => (
                <li key={column} className="flex justify-between">
                  <span>{column}</span>
                  <span className="text-slate-500 dark:text-slate-400">
                    {stats.unique_values} unique · top: {stats.top_value ?? 'N/A'}
                  </span>
                </li>
              ))}
            </ul>
          </CollapsibleSection>
        )}
      </section>

      {Object.keys(previews).length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            📂 Uploaded Datasets
          </h2>
          <div className="space-y-3">
            {tables.map((table) => (
              <CollapsibleSection
                key={table.table_name}
                title={`📄 ${table.table_name} | ${table.rows} rows | ${table.columns} columns`}
              >
                <DataTable rows={previews[table.table_name] ?? []} />
              </CollapsibleSection>
            ))}
          </div>
        </section>
      )}

      {relationships.length > 0 && (
        <section>
          <h2 className="mb-1 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            🔗 Relationship Explorer
          </h2>
          <p className="mb-3 text-sm text-emerald-700 dark:text-emerald-400">
            Detected {relationships.length} relationship(s)
          </p>
          <div className="space-y-2">
            {relationships.map((rel, index) => (
              <div
                key={index}
                className="rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm dark:border-slate-700 dark:bg-slate-800"
              >
                <span className="font-medium text-slate-800 dark:text-slate-200">
                  {rel.left_table}.{rel.left_column}
                </span>
                <span className="mx-2 text-slate-400 dark:text-slate-500">➡️</span>
                <span className="font-medium text-slate-800 dark:text-slate-200">
                  {rel.right_table}.{rel.right_column}
                </span>
                {rel.relationship && (
                  <span className="ml-2 text-slate-500 dark:text-slate-400">
                    ({rel.relationship})
                  </span>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {tables.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            📊 Data Model Summary
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <StatCard label="Tables" value={tables.length} />
            <StatCard label="Relationships" value={relationships.length} />
            <StatCard label="Total Rows" value={totalRows} />
          </div>
          <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
            {tables.map((table) => (
              <div
                key={table.table_name}
                className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
              >
                {table.table_name} ({table.rows} rows, {table.columns} columns)
              </div>
            ))}
          </div>
        </section>
      )}

      {insightEntries.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            📊 AI Generated Insights
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {insightEntries.map(([key, value]) => (
              <StatCard
                key={key}
                label={titleCase(key)}
                value={typeof value === 'object' ? JSON.stringify(value) : String(value)}
              />
            ))}
          </div>
        </section>
      )}

      {Boolean(insights.error) && (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-800 dark:bg-red-950/40 dark:text-red-300">
          {String(insights.error)}
        </div>
      )}

      {suggested_questions.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Suggested Questions
          </h2>
          <div className="space-y-2">
            {suggested_questions.map((question, index) => (
              <div
                key={index}
                className="rounded-md border border-sky-200 bg-sky-50 px-3 py-2 text-sm text-sky-800 dark:border-sky-800 dark:bg-sky-950/40 dark:text-sky-300"
              >
                {question}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
