"""Add email_campaigns table for bulk email sending

Revision ID: 20251111_email_campaigns
Revises: 20251111_page_content
Create Date: 2025-11-11 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251111_email_campaigns'
down_revision = '20251111_page_content'
branch_labels = None
depends_on = None


def upgrade():
    # Check if table exists before creating it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create email_campaigns table if not exists
    if 'email_campaigns' not in existing_tables:
        op.create_table('email_campaigns',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('nom', sa.String(length=200), nullable=False),
            sa.Column('sujet', sa.String(length=300), nullable=False),
            sa.Column('contenu_html', sa.Text(), nullable=False),
            sa.Column('contenu_texte', sa.Text(), nullable=True),
            sa.Column('statut', sa.String(length=50), nullable=True),
            sa.Column('emails_total', sa.Integer(), nullable=True),
            sa.Column('emails_envoyes', sa.Integer(), nullable=True),
            sa.Column('emails_erreurs', sa.Integer(), nullable=True),
            sa.Column('date_creation', sa.DateTime(), nullable=True),
            sa.Column('date_envoi', sa.DateTime(), nullable=True),
            sa.Column('date_fin_envoi', sa.DateTime(), nullable=True),
            sa.Column('created_by_user_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # Only drop table if it exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'email_campaigns' in existing_tables:
        op.drop_table('email_campaigns')
