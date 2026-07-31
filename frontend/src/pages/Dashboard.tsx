import axios from "axios";
import { useEffect, useState } from "react";

import {
  getCostHistory,
  getDashboardSummary,
  getExperimentResults,
  getJudgeScoreHistory,
  getLatencyHistory,
  getTokenHistory,
} from "../api/dashboard";

import type {
  CostHistoryItem,
  DashboardSummary,
  ExperimentResult,
  JudgeScoreHistoryItem,
  LatencyHistoryItem,
  TokenHistoryItem,
} from "../api/dashboard";

import DashboardCharts from "../components/DashboardCharts";
import ResultsTable from "../components/ResultsTable";
import SummaryCards from "../components/SummaryCards";

import "./Dashboard.css";

export default function Dashboard() {
  const [experimentId, setExperimentId] = useState(3);
  const [selectedExperimentId, setSelectedExperimentId] =
    useState(3);

  const [results, setResults] = useState<ExperimentResult[]>([]);
  const [summary, setSummary] =
    useState<DashboardSummary | null>(null);

  const [costHistory, setCostHistory] = useState<
    CostHistoryItem[]
  >([]);

  const [latencyHistory, setLatencyHistory] = useState<
    LatencyHistoryItem[]
  >([]);

  const [judgeHistory, setJudgeHistory] = useState<
    JudgeScoreHistoryItem[]
  >([]);

  const [tokenHistory, setTokenHistory] = useState<
    TokenHistoryItem[]
  >([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const [
          summaryData,
          costData,
          latencyData,
          judgeData,
          tokenData,
          resultsData,
        ] = await Promise.all([
          getDashboardSummary(selectedExperimentId),
          getCostHistory(selectedExperimentId),
          getLatencyHistory(selectedExperimentId),
          getJudgeScoreHistory(selectedExperimentId),
          getTokenHistory(selectedExperimentId),
          getExperimentResults(selectedExperimentId),
        ]);

        setSummary(summaryData);
        setCostHistory(costData);
        setLatencyHistory(latencyData);
        setJudgeHistory(judgeData);
        setTokenHistory(tokenData);
        setResults(resultsData);
      } catch (requestError: unknown) {
        if (axios.isAxiosError(requestError)) {
          const detail = requestError.response?.data?.detail;

          setError(
            typeof detail === "string"
              ? detail
              : requestError.message,
          );
        } else {
          setError("An unexpected error occurred.");
        }
      } finally {
        setLoading(false);
      }
    }

    void loadDashboard();
  }, [selectedExperimentId]);

  function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!Number.isInteger(experimentId) || experimentId < 1) {
      setError(
        "Experiment ID must be a whole number greater than zero.",
      );
      return;
    }

    setError("");
    setSelectedExperimentId(experimentId);
  }

  return (
    <main className="dashboard-page">
      <div className="dashboard-background-shape dashboard-shape-one" />
      <div className="dashboard-background-shape dashboard-shape-two" />

      <header className="dashboard-header">
        <section className="dashboard-heading">
          <div className="platform-badge">
            <span className="platform-badge-icon">✦</span>
            AI Reliability Platform
          </div>

          <h1>LLM Evaluation Dashboard</h1>

          <p className="dashboard-description">
            Monitor evaluation quality, latency, token usage, and
            cost across your experiments.
          </p>
        </section>

        <section className="dashboard-controls">
          <form
            className="experiment-form"
            onSubmit={handleSubmit}
          >
            <label htmlFor="experiment-id">
              Experiment ID
            </label>

            <div className="experiment-form-row">
              <input
                id="experiment-id"
                min="1"
                step="1"
                type="number"
                value={experimentId}
                onChange={(event) =>
                  setExperimentId(
                    Number(event.target.value),
                  )
                }
              />

              <button
                type="submit"
                disabled={loading}
              >
                <span className="load-button-icon">
                  {loading ? "◌" : "↗"}
                </span>

                {loading ? "Loading" : "Load"}
              </button>
            </div>
          </form>

          <div className="experiment-status">
            <span className="experiment-model">
              Experiment #{selectedExperimentId}
            </span>

            <span className="status-dot" />

            <span className="status-text">
              {loading ? "Loading" : "Completed"}
            </span>
          </div>
        </section>

        <div
          className="dashboard-robot"
          aria-hidden="true"
        >
          <div className="robot-antenna">
            <span />
          </div>

          <div className="robot-head">
            <div className="robot-face">
              <span className="robot-eye" />
              <span className="robot-eye" />
            </div>
          </div>

          <div className="robot-body">
            <span className="robot-chart-bar bar-one" />
            <span className="robot-chart-bar bar-two" />
            <span className="robot-chart-bar bar-three" />
          </div>
        </div>
      </header>

      {loading && (
        <section
          className="dashboard-loading"
          aria-live="polite"
        >
          <div className="loading-spinner" />

          <div>
            <h2>Loading experiment data</h2>
            <p>
              Collecting metrics, scores, costs, and results.
            </p>
          </div>
        </section>
      )}

      {!loading && error && (
        <section
          className="dashboard-error"
          role="alert"
        >
          <div className="error-icon">!</div>

          <div>
            <h2>Unable to load dashboard</h2>
            <p>{error}</p>
          </div>

          <button
            type="button"
            onClick={() =>
              setSelectedExperimentId(experimentId)
            }
          >
            Try again
          </button>
        </section>
      )}

      {!loading && !error && summary && (
        <div className="dashboard-content">
          <SummaryCards summary={summary} />

          <DashboardCharts
            costHistory={costHistory}
            latencyHistory={latencyHistory}
            judgeHistory={judgeHistory}
            tokenHistory={tokenHistory}
          />

          <ResultsTable results={results} />
        </div>
      )}
    </main>
  );
}