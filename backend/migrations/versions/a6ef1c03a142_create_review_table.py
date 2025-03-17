"""Create review table

Revision ID: a6ef1c03a142
Revises: 2b2b7dda7827
Create Date: 2025-03-17 22:08:49.745447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6ef1c03a142'
down_revision: Union[str, None] = '2b2b7dda7827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply the schema changes."""
    op.create_table(
        'review',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.id'), nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('comment', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )


def downgrade() -> None:
    """Revert the schema changes."""
    op.drop_table('review')
