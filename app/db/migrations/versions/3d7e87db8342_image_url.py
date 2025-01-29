"""image_url

Revision ID: 3d7e87db8342
Revises: 649592bb9e57
Create Date: 2025-01-29 18:41:15.059876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d7e87db8342'
down_revision = '649592bb9e57'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('songs', 'image_url')
    # ### end Alembic commands ###
