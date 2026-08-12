from sqlalchemy.orm import Session

from app.experiments.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def summary(self, experiment_id: int):
        return self.repository.get_summary(experiment_id)

    def cost_history(self, experiment_id: int):
        return self.repository.get_cost_history(experiment_id)

    def latency_history(self, experiment_id: int):
        return self.repository.get_latency_history(experiment_id)

    def judge_score_history(self, experiment_id: int):
        return self.repository.get_judge_score_history(experiment_id)

    def token_history(self, experiment_id: int):
        return self.repository.get_token_history(experiment_id)