"""Added foreign key to reviews and modified users table

Revision ID: 643a78ea7c57
Revises: a6ef1c03a142
Create Date: 2025-03-21 21:31:31.615790
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = '643a78ea7c57'
down_revision: Union[str, None] = 'a6ef1c03a142'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema by modifying the users table."""

    # Step 1: Create a new temporary users table with the correct schema
    op.create_table(
        "users_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), unique=True, nullable=False),
        sa.Column("role", sa.String(), nullable=False),
    )

    # Step 2: Copy existing data from old users table to users_temp
    op.execute(
        "INSERT INTO users_temp (id, username, email, role) SELECT id, username, email, role FROM users"
    )

    # Step 3: Drop the old users table
    op.drop_table("users")

    # Step 4: Rename users_temp to users (new structure is now applied)
    op.rename_table("users_temp", "users")


def downgrade() -> None:
    """Revert schema changes (restore old users table)."""

    # Step 1: Recreate the old users table with its previous structure
    op.create_table(
        "users_old",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), unique=True, nullable=True),
        sa.Column("role", sa.String(), nullable=True),
    )

    # Step 2: Copy data back from modified users table to old users structure
    op.execute(
        "INSERT INTO users_old (id, username, email, role) SELECT id, username, email, role FROM users"
    )

    # Step 3: Drop the modified users table
    op.drop_table("users")

    # Step 4: Rename users_old back to users
    op.rename_table("users_old", "users")
