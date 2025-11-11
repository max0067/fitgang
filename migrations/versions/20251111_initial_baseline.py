"""Initial baseline migration

Revision ID: 20251111_baseline
Revises:
Create Date: 2025-11-11 10:58:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251111_baseline'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if tables exist before creating them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create users table if not exists
    if 'users' not in existing_tables:
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('nom', sa.String(length=100), nullable=False),
            sa.Column('prenom', sa.String(length=100), nullable=False),
            sa.Column('password_hash', sa.String(length=256), nullable=False),
            sa.Column('is_admin', sa.Boolean(), nullable=True),
            sa.Column('date_inscription', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )

    # Create programmes table if not exists
    if 'programmes' not in existing_tables:
        op.create_table('programmes',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('titre', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('prix', sa.Float(), nullable=False),
            sa.Column('niveau', sa.String(length=50), nullable=True),
            sa.Column('duree', sa.String(length=100), nullable=True),
            sa.Column('image', sa.String(length=500), nullable=True),
            sa.Column('contenu', sa.Text(), nullable=True),
            sa.Column('actif', sa.Boolean(), nullable=True),
            sa.Column('date_creation', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create ebooks table if not exists
    if 'ebooks' not in existing_tables:
        op.create_table('ebooks',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('titre', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('prix', sa.Float(), nullable=False),
            sa.Column('fichier', sa.String(length=500), nullable=False),
            sa.Column('image', sa.String(length=500), nullable=True),
            sa.Column('nombre_pages', sa.Integer(), nullable=True),
            sa.Column('actif', sa.Boolean(), nullable=True),
            sa.Column('date_creation', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create achats table if not exists
    if 'achats' not in existing_tables:
        op.create_table('achats',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('type', sa.String(length=50), nullable=False),
            sa.Column('item_id', sa.Integer(), nullable=False),
            sa.Column('prix_paye', sa.Float(), nullable=False),
            sa.Column('date_achat', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Create photos table if not exists
    if 'photos' not in existing_tables:
        op.create_table('photos',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('type', sa.String(length=10), nullable=False),
            sa.Column('fichier', sa.String(length=500), nullable=False),
            sa.Column('poids', sa.Float(), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('visible_public', sa.Boolean(), nullable=True),
            sa.Column('date_upload', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Create progressions table if not exists
    if 'progressions' not in existing_tables:
        op.create_table('progressions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('date_seance', sa.DateTime(), nullable=False),
            sa.Column('exercice', sa.String(length=200), nullable=False),
            sa.Column('series', sa.Integer(), nullable=True),
            sa.Column('repetitions', sa.Integer(), nullable=True),
            sa.Column('poids', sa.Float(), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('date_ajout', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # Only drop tables that were created in upgrade
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'progressions' in existing_tables:
        op.drop_table('progressions')
    if 'photos' in existing_tables:
        op.drop_table('photos')
    if 'achats' in existing_tables:
        op.drop_table('achats')
    if 'ebooks' in existing_tables:
        op.drop_table('ebooks')
    if 'programmes' in existing_tables:
        op.drop_table('programmes')
    if 'users' in existing_tables:
        op.drop_table('users')
