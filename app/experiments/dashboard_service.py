from sqlalchemy.orm import Session

from app.experiments.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db: Session):
        self.repo = DashboardRepository(db)

    def summary(self, experiment_id: int):
        return self.repo.get_summary(experiment_id)