"""Add blog_posts table

Revision ID: add_blog_posts
Revises:
Create Date: 2025-11-19

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'add_blog_posts'
down_revision = None  # Mettre l'ID de la dernière migration si elle existe
branch_labels = None
depends_on = None


def upgrade():
    # Créer la table blog_posts
    op.create_table('blog_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titre', sa.String(length=300), nullable=False),
        sa.Column('slug', sa.String(length=350), nullable=False),
        sa.Column('contenu', sa.Text(), nullable=False),
        sa.Column('extrait', sa.Text(), nullable=True),
        sa.Column('image_principale', sa.String(length=500), nullable=True),
        sa.Column('auteur_id', sa.Integer(), nullable=True),
        sa.Column('categorie', sa.String(length=100), nullable=True),
        sa.Column('tags', sa.String(length=500), nullable=True),
        sa.Column('vues', sa.Integer(), nullable=True, default=0),
        sa.Column('publie', sa.Boolean(), nullable=True, default=True),
        sa.Column('date_creation', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('date_modification', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('date_publication', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['auteur_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Créer les index
    op.create_index(op.f('ix_blog_posts_slug'), 'blog_posts', ['slug'], unique=True)


def downgrade():
    # Supprimer les index
    op.drop_index(op.f('ix_blog_posts_slug'), table_name='blog_posts')

    # Supprimer la table
    op.drop_table('blog_posts')
