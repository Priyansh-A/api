"""adding columns

Revision ID: 762b789b33d3
Revises: 4c773267ebd3
Create Date: 2026-01-23 21:49:03.781147

"""
import sqlmodel
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '762b789b33d3'
down_revision: Union[str, Sequence[str], None] = '4c773267ebd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))   
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    pass
