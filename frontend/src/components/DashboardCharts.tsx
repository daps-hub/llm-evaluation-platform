import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

import type {
  CostHistoryItem,
  JudgeScoreHistoryItem,
  LatencyHistoryItem,
  TokenHistoryItem,
} from "../api/dashboard";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

interface DashboardChartsProps {
  costHistory: CostHistoryItem[];
  latencyHistory: LatencyHistoryItem[];
  judgeHistory: JudgeScoreHistoryItem[];
  tokenHistory: TokenHistoryItem[];
}

const commonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top" as const,
    },
  },
};

export default function DashboardCharts({
  costHistory,
  latencyHistory,
  judgeHistory,
  tokenHistory,
}: DashboardChartsProps) {
  return (
    <section className="chart-grid">
      <article className="chart-card">
        <h2>Cost History</h2>

        <div className="chart-container">
          <Line
            options={commonOptions}
            data={{
              labels: costHistory.map((item, index) =>
                item.result_id ? `Result ${item.result_id}` : `Run ${index + 1}`,
              ),
              datasets: [
                {
                  label: "Generation Cost",
                  data: costHistory.map(
                    (item) => item.generation_cost ?? 0,
                  ),
                },
                {
                  label: "Judge Cost",
                  data: costHistory.map((item) => item.judge_cost ?? 0),
                },
                {
                  label: "Total Cost",
                  data: costHistory.map((item) => item.total_cost ?? 0),
                },
              ],
            }}
          />
        </div>
      </article>

      <article className="chart-card">
        <h2>Latency History</h2>

        <div className="chart-container">
          <Line
            options={commonOptions}
            data={{
              labels: latencyHistory.map(
                (_, index) => `Run ${index + 1}`,
              ),
              datasets: [
                {
                  label: "Latency (ms)",
                  data: latencyHistory.map(
                    (item) => item.latency_ms ?? 0,
                  ),
                },
              ],
            }}
          />
        </div>
      </article>

      <article className="chart-card">
        <h2>Judge Score History</h2>

        <div className="chart-container">
          <Line
            options={commonOptions}
            data={{
              labels: judgeHistory.map((_, index) => `Run ${index + 1}`),
              datasets: [
                {
                  label: "Judge Score",
                  data: judgeHistory.map(
                    (item) => item.judge_score ?? 0,
                  ),
                },
              ],
            }}
          />
        </div>
      </article>

      <article className="chart-card">
        <h2>Token History</h2>

        <div className="chart-container">
          <Line
            options={commonOptions}
            data={{
              labels: tokenHistory.map((_, index) => `Run ${index + 1}`),
              datasets: [
                {
                  label: "Input Tokens",
                  data: tokenHistory.map(
                    (item) => item.input_tokens ?? 0,
                  ),
                },
                {
                  label: "Output Tokens",
                  data: tokenHistory.map(
                    (item) => item.output_tokens ?? 0,
                  ),
                },
                {
                  label: "Total Tokens",
                  data: tokenHistory.map(
                    (item) => item.total_tokens ?? 0,
                  ),
                },
              ],
            }}
          />
        </div>
      </article>
    </section>
  );
}