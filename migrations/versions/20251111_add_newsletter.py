"""Add newsletter table

Revision ID: 20251111_newsletter
Revises: 20251111_complements
Create Date: 2025-11-11 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251111_newsletter'
down_revision = '20251111_complements'
branch_labels = None
depends_on = None


def upgrade():
    # Check if table exists before creating it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create newsletter table if not exists
    if 'newsletter' not in existing_tables:
        op.create_table('newsletter',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('date_inscription', sa.DateTime(), nullable=True),
            sa.Column('actif', sa.Boolean(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )

        # Create index on email
        op.create_index('ix_newsletter_email', 'newsletter', ['email'], unique=True)


def downgrade():
    # Only drop table if it exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'newsletter' in existing_tables:
        op.drop_index('ix_newsletter_email', table_name='newsletter')
        op.drop_table('newsletter')
