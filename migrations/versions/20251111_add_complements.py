"""Add complements table

Revision ID: 20251111_complements
Revises: 20251111_seances
Create Date: 2025-11-11 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251111_complements'
down_revision = '20251111_seances'
branch_labels = None
depends_on = None


def upgrade():
    # Check if table exists before creating it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create complements table if not exists
    if 'complements' not in existing_tables:
        op.create_table('complements',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('nom', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('prix', sa.Float(), nullable=False),
            sa.Column('image', sa.String(length=300), nullable=True),
            sa.Column('categorie', sa.String(length=100), nullable=True),
            sa.Column('marque', sa.String(length=100), nullable=True),
            sa.Column('dosage', sa.String(length=200), nullable=True),
            sa.Column('lien_achat', sa.String(length=500), nullable=True),
            sa.Column('actif', sa.Boolean(), nullable=True),
            sa.Column('date_creation', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # Only drop table if it exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'complements' in existing_tables:
        op.drop_table('complements')
