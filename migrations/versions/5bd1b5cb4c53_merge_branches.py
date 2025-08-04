"""merge branches

Revision ID: 5bd1b5cb4c53
Revises: 157e52561b8a, 3d91c8ad3a43
Create Date: 2025-07-31 12:18:46.784609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bd1b5cb4c53'
down_revision = ('157e52561b8a', '3d91c8ad3a43')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
