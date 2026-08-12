import { useMemo, useState } from "react"

import type { ExperimentResult } from "../api/dashboard"

interface ResultsTableProps {
  results: ExperimentResult[]
}

type MetricKind =
  | "success"
  | "warning"
  | "danger"
  | "neutral"

function formatNumber(
  value: number | null | undefined,
  digits = 2,
): string {
  if (value === null || value === undefined) {
    return "N/A"
  }

  return value.toFixed(digits)
}

function formatCost(
  value: number | null | undefined,
): string {
  if (value === null || value === undefined) {
    return "N/A"
  }

  return `$${value.toFixed(6)}`
}

function formatLatency(
  value: number | null | undefined,
): string {
  if (value === null || value === undefined) {
    return "N/A"
  }

  return `${value.toLocaleString()} ms`
}

function truncate(
  value: string | null | undefined,
  maximumLength = 85,
): string {
  if (!value) {
    return "N/A"
  }

  if (value.length <= maximumLength) {
    return value
  }

  return `${value.slice(0, maximumLength)}…`
}

function getExactMatchKind(
  value: number | null | undefined,
): MetricKind {
  if (value === null || value === undefined) {
    return "neutral"
  }

  return value >= 1 ? "success" : "danger"
}

function getSimilarityKind(
  value: number | null | undefined,
): MetricKind {
  if (value === null || value === undefined) {
    return "neutral"
  }

  if (value >= 0.8) {
    return "success"
  }

  if (value >= 0.5) {
    return "warning"
  }

  return "danger"
}

function getJudgeKind(
  value: number | null | undefined,
): MetricKind {
  if (value === null || value === undefined) {
    return "neutral"
  }

  if (value >= 8) {
    return "success"
  }

  if (value >= 5) {
    return "warning"
  }

  return "danger"
}

export default function ResultsTable({
  results,
}: ResultsTableProps) {
  const [search, setSearch] = useState("")

  const filteredResults = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase()

    if (!normalizedSearch) {
      return results
    }

    return results.filter((result) => {
      const searchableText = [
        result.id,
        result.dataset_item_id,
        result.prompt,
        result.expected_output,
        result.model_output,
        result.judge_reasoning,
      ]
        .filter(
          (value) =>
            value !== null &&
            value !== undefined,
        )
        .join(" ")
        .toLowerCase()

      return searchableText.includes(normalizedSearch)
    })
  }, [results, search])

  if (results.length === 0) {
    return (
      <section className="results-section">
        <div className="empty-results">
          <div className="empty-results-icon">⌁</div>

          <h2>No evaluation results</h2>

          <p>
            Run this experiment to generate detailed
            evaluation data.
          </p>
        </div>
      </section>
    )
  }

  return (
    <section className="results-section">
      <header className="results-header">
        <div className="results-heading">
          <div className="results-title-icon">
            ☷
          </div>

          <div>
            <p className="section-eyebrow">
              Evaluation details
            </p>

            <h2>Experiment Results</h2>
          </div>
        </div>

        <div className="results-actions">
          <span className="result-count">
            {filteredResults.length} result
            {filteredResults.length === 1 ? "" : "s"}
          </span>

          <label className="results-search">
            <span aria-hidden="true">⌕</span>

            <input
              type="search"
              value={search}
              placeholder="Search results"
              aria-label="Search experiment results"
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />
          </label>

          <button
            type="button"
            className="results-action-button"
          >
            <span aria-hidden="true">⇩</span>
            Export
          </button>
        </div>
      </header>

      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Result</th>
              <th>Dataset Item</th>
              <th>Prompt</th>
              <th>Expected</th>
              <th>Response</th>
              <th>Exact Match</th>
              <th>Similarity</th>
              <th>Judge</th>
              <th>Latency</th>
              <th>Tokens</th>
              <th>Total Cost</th>
            </tr>
          </thead>

          <tbody>
            {filteredResults.map((result) => {
              const displayedCost =
                result.total_cost ?? result.cost

              return (
                <tr key={result.id}>
                  <td>
                    <span className="result-id">
                      #{result.id}
                    </span>
                  </td>

                  <td>
                    <span className="dataset-item-badge">
                      #{result.dataset_item_id}
                    </span>
                  </td>

                  <td
                    className="text-cell"
                    title={result.prompt ?? ""}
                  >
                    {truncate(result.prompt)}
                  </td>

                  <td
                    className="text-cell expected-cell"
                    title={
                      result.expected_output ?? ""
                    }
                  >
                    {truncate(
                      result.expected_output,
                      60,
                    )}
                  </td>

                  <td
                    className="text-cell response-cell"
                    title={result.model_output ?? ""}
                  >
                    {truncate(
                      result.model_output,
                      95,
                    )}
                  </td>

                  <td>
                    <MetricBadge
                      value={formatNumber(
                        result.exact_match_score,
                      )}
                      kind={getExactMatchKind(
                        result.exact_match_score,
                      )}
                    />
                  </td>

                  <td>
                    <MetricBadge
                      value={formatNumber(
                        result.semantic_similarity_score,
                      )}
                      kind={getSimilarityKind(
                        result.semantic_similarity_score,
                      )}
                    />
                  </td>

                  <td>
                    <MetricBadge
                      value={formatNumber(
                        result.judge_score,
                      )}
                      kind={getJudgeKind(
                        result.judge_score,
                      )}
                    />
                  </td>

                  <td>
                    <span className="latency-value">
                      {formatLatency(
                        result.latency_ms,
                      )}
                    </span>
                  </td>

                  <td>
                    <span className="token-badge">
                      {result.total_tokens ?? "N/A"}
                    </span>
                  </td>

                  <td>
                    <span className="cost-value">
                      {formatCost(displayedCost)}
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {filteredResults.length === 0 && (
        <div className="filtered-empty-state">
          No results match “{search}”.
        </div>
      )}
    </section>
  )
}

interface MetricBadgeProps {
  value: string
  kind: MetricKind
}

function MetricBadge({
  value,
  kind,
}: MetricBadgeProps) {
  return (
    <span className={`metric-badge ${kind}`}>
      {value}
    </span>
  )
}