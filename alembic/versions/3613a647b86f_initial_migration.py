"""initial migration

Revision ID: 3613a647b86f
Revises: 
Create Date: 2026-01-23 21:00:13.143535

"""
import sqlmodel
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3613a647b86f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))  
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'address')
    pass
    # ### end Alembic commands ###
