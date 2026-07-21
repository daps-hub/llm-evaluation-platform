"""add provider and expected actual responses

Revision ID: d6fde6f723bf
Revises: 90b2da59faf7
Create Date: 2026-07-20 18:31:51.537020
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6fde6f723bf"
down_revision: str | None = "90b2da59faf7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply the migration."""

    # Give existing rows a temporary provider value.
    op.add_column(
        "evaluations",
        sa.Column(
            "provider",
            sa.String(length=50),
            nullable=False,
            server_default="mock",
        ),
    )

    op.add_column(
        "evaluations",
        sa.Column(
            "expected_response",
            sa.Text(),
            nullable=True,
        ),
    )

    # Preserve existing response data by renaming the column.
    op.alter_column(
        "evaluations",
        "response",
        new_column_name="actual_response",
        existing_type=sa.Text(),
        existing_nullable=False,
    )

    # The application supplies the provider value from now on.
    op.alter_column(
        "evaluations",
        "provider",
        server_default=None,
        existing_type=sa.String(length=50),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Reverse the migration."""

    # Restore the original column name without losing data.
    op.alter_column(
        "evaluations",
        "actual_response",
        new_column_name="response",
        existing_type=sa.Text(),
        existing_nullable=False,
    )

    op.drop_column(
        "evaluations",
        "expected_response",
    )

    op.drop_column(
        "evaluations",
        "provider",
    )