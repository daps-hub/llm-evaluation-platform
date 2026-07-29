"""change judge score to float

Revision ID: 9bfac3eb92f9
Revises: deac6a5f712a
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "9bfac3eb92f9"
down_revision: str | None = "deac6a5f712a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply the migration."""
    op.alter_column(
        "experiment_results",
        "judge_score",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using="judge_score::double precision",
    )


def downgrade() -> None:
    """Reverse the migration."""
    op.alter_column(
        "experiment_results",
        "judge_score",
        existing_type=sa.Float(),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True,
        postgresql_using="judge_score::varchar",
    )