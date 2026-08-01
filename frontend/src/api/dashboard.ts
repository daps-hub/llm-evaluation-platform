import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ??
    "http://127.0.0.1:8000",
  timeout: 30000,
});

export interface DashboardSummary {
  total_runs: number;
  average_latency_ms: number | null;
  average_tokens: number | null;
  average_cost: number | null;
  average_exact_match: number | null;
  average_semantic_similarity: number | null;
  average_judge_score: number | null;
}

export interface CostHistoryItem {
  result_id: number;
  generation_cost: number | null;
  judge_cost: number | null;
  total_cost: number | null;
}

export interface LatencyHistoryItem {
  result_id?: number;
  latency_ms: number | null;
}

export interface JudgeScoreHistoryItem {
  result_id?: number;
  judge_score: number | null;
}

export interface TokenHistoryItem {
  result_id?: number;
  input_tokens: number | null;
  output_tokens: number | null;
  total_tokens: number | null;
}

export async function getDashboardSummary(
  experimentId: number,
): Promise<DashboardSummary> {
  const response = await api.get<DashboardSummary>(
    `/experiments/${experimentId}/dashboard`,
  );

  return response.data;
}

export async function getCostHistory(
  experimentId: number,
): Promise<CostHistoryItem[]> {
  const response = await api.get<CostHistoryItem[]>(
    `/experiments/${experimentId}/dashboard/cost-history`,
  );

  return response.data;
}

export async function getLatencyHistory(
  experimentId: number,
): Promise<LatencyHistoryItem[]> {
  const response = await api.get<LatencyHistoryItem[]>(
    `/experiments/${experimentId}/dashboard/latency-history`,
  );

  return response.data;
}

export async function getJudgeScoreHistory(
  experimentId: number,
): Promise<JudgeScoreHistoryItem[]> {
  const response = await api.get<JudgeScoreHistoryItem[]>(
    `/experiments/${experimentId}/dashboard/judge-score-history`,
  );

  return response.data;
}

export async function getTokenHistory(
  experimentId: number,
): Promise<TokenHistoryItem[]> {
  const response = await api.get<TokenHistoryItem[]>(
    `/experiments/${experimentId}/dashboard/token-history`,
  );

  return response.data;
}

export interface ExperimentResult {
  id: number
  experiment_id: number
  dataset_item_id: number

  model_output: string | null

  input_tokens: number | null
  output_tokens: number | null
  total_tokens: number | null

  cost: number | null
  generation_cost: number | null
  judge_cost: number | null
  total_cost: number | null

  latency_ms: number | null

  exact_match_score: number | null
  semantic_similarity_score: number | null
  judge_score: number | null
  judge_reasoning: string | null

  error_message: string | null
  created_at: string

  prompt?: string | null
  expected_output?: string | null
}
export async function getExperimentResults(
  experimentId: number,
): Promise<ExperimentResult[]> {
  const response = await api.get<ExperimentResult[]>(
    `/experiments/${experimentId}/results`,
  )

  return response.data
}