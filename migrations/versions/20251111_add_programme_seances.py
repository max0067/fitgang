"""Add programme seances and progressions tables

Revision ID: 20251111_seances
Revises: 20251111_baseline
Create Date: 2025-11-11 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251111_seances'
down_revision = '20251111_baseline'
branch_labels = None
depends_on = None


def upgrade():
    # Check if tables exist before creating them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create programme_seances table if not exists
    if 'programme_seances' not in existing_tables:
        op.create_table('programme_seances',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('programme_id', sa.Integer(), nullable=False),
            sa.Column('semaine', sa.Integer(), nullable=False),
            sa.Column('jour', sa.Integer(), nullable=False),
            sa.Column('titre', sa.String(length=200), nullable=False),
            sa.Column('exercices', sa.Text(), nullable=False),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('ordre', sa.Integer(), nullable=True),
            sa.Column('date_creation', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['programme_id'], ['programmes.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # Create programme_progressions table if not exists
    if 'programme_progressions' not in existing_tables:
        op.create_table('programme_progressions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('programme_seance_id', sa.Integer(), nullable=False),
            sa.Column('completed', sa.Boolean(), nullable=True),
            sa.Column('date_completed', sa.DateTime(), nullable=True),
            sa.Column('poids', sa.Float(), nullable=True),
            sa.Column('notes_perso', sa.Text(), nullable=True),
            sa.ForeignKeyConstraint(['programme_seance_id'], ['programme_seances.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # Only drop tables that were created in upgrade
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'programme_progressions' in existing_tables:
        op.drop_table('programme_progressions')
    if 'programme_seances' in existing_tables:
        op.drop_table('programme_seances')
