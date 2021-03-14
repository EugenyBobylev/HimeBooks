"""Catalog table

Revision ID: d447822fca82
Revises: d57b3e25b0c1
Create Date: 2021-03-14 18:32:21.383542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd447822fca82'
down_revision = 'd57b3e25b0c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catalog',
    sa.Column('catalog', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('catalog')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('catalog')
    # ### end Alembic commands ###
