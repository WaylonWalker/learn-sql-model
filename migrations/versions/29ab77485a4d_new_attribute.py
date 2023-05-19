"""New Attribute

Revision ID: 29ab77485a4d
Revises: fe841f5746e5
Create Date: 2023-05-18 11:09:53.112601

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '29ab77485a4d'
down_revision = 'fe841f5746e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hero', sa.Column('new_attribute', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hero', 'new_attribute')
    # ### end Alembic commands ###
