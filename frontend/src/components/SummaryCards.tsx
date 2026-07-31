import type { DashboardSummary } from "../api/dashboard";

interface SummaryCardsProps {
  summary: DashboardSummary;
}

function formatNumber(value: number | null, digits = 2): string {
  if (value === null || value === undefined) {
    return "N/A";
  }

  return value.toFixed(digits);
}

export default function SummaryCards({ summary }: SummaryCardsProps) {
  const cards = [
    {
      title: "Total Runs",
      value: summary.total_runs.toString(),
    },
    {
      title: "Average Cost",
      value:
        summary.average_cost === null
          ? "N/A"
          : `$${summary.average_cost.toFixed(6)}`,
    },
    {
      title: "Average Latency",
      value:
        summary.average_latency_ms === null
          ? "N/A"
          : `${formatNumber(summary.average_latency_ms, 0)} ms`,
    },
    {
      title: "Average Tokens",
      value: formatNumber(summary.average_tokens, 0),
    },
    {
      title: "Exact Match",
      value: formatNumber(summary.average_exact_match),
    },
    {
      title: "Semantic Similarity",
      value: formatNumber(summary.average_semantic_similarity),
    },
    {
      title: "Judge Score",
      value: formatNumber(summary.average_judge_score),
    },
  ];

  return (
    <section className="summary-grid">
      {cards.map((card) => (
        <article className="summary-card" key={card.title}>
          <p className="summary-card-title">{card.title}</p>
          <p className="summary-card-value">{card.value}</p>
        </article>
      ))}
    </section>
  );
}