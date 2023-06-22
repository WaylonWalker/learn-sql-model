"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from learn_sql_model.er_diagram import generate_er_diagram, generate_er_markdown
from learn_sql_model.config import get_config

${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
    generate_er_diagram(f'migrations/versions/{revision}_er_diagram.png')
    generate_er_markdown(f'migrations/versions/{revision}_er_diagram.md', f'migrations/versions/er_diagram_{revision}.png')


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
