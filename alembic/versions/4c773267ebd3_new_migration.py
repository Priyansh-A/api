"""new migration

Revision ID: 4c773267ebd3
Revises: 3613a647b86f
Create Date: 2026-01-23 21:25:49.020321

"""
import sqlmodel
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c773267ebd3'
down_revision: Union[str, Sequence[str], None] = '3613a647b86f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))   
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'age')
    pass