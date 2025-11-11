"""Add page_content table for homepage customization

Revision ID: 20251111_page_content
Revises: 20251111_newsletter
Create Date: 2025-11-11 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '20251111_page_content'
down_revision = '20251111_newsletter'
branch_labels = None
depends_on = None


def upgrade():
    # Check if table exists before creating it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create page_content table if not exists
    if 'page_content' not in existing_tables:
        op.create_table('page_content',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('section', sa.String(length=100), nullable=False),
            sa.Column('contenu', sa.Text(), nullable=False),
            sa.Column('date_modification', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('section')
        )

        # Create index on section
        op.create_index('ix_page_content_section', 'page_content', ['section'], unique=True)

        # Insert default content
        page_content_table = sa.table('page_content',
            sa.column('section', sa.String),
            sa.column('contenu', sa.Text),
            sa.column('date_modification', sa.DateTime)
        )

        default_content = [
            {
                'section': 'hero_titre',
                'contenu': 'TRANSFORME TON CORPS,<br><span class="text-danger">DÉPASSE TES LIMITES</span>',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'hero_sous_titre',
                'contenu': 'Rejoins FitGang et découvre des programmes exclusifs pour atteindre tes objectifs fitness. Nutrition, entraînement, mindset : tout pour réussir ta transformation.',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'stat_membres',
                'contenu': '10K+ Membres Actifs',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'stat_programmes',
                'contenu': '50+ Programmes',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'stat_transformations',
                'contenu': '1000+ Transformations',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'stat_satisfaction',
                'contenu': '98% Satisfaction',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'philosophie_titre',
                'contenu': 'PLUS QU\'UNE SALLE,<br><span class="text-danger">UN MODE DE VIE</span>',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'philosophie_texte',
                'contenu': 'Chez FitGang, on croit que le fitness n\'est pas qu\'une question de physique. C\'est un état d\'esprit, une discipline, une détermination à devenir la meilleure version de soi-même. Nos programmes ne se contentent pas de te donner des exercices. Ils te forgent mentalement, te poussent à dépasser tes limites et te font rejoindre une communauté de guerriers qui partagent la même passion.',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'cta_titre',
                'contenu': 'PRÊT À COMMENCER<br><span class="text-danger">TA TRANSFORMATION ?</span>',
                'date_modification': datetime.utcnow()
            },
            {
                'section': 'cta_texte',
                'contenu': 'Rejoins des milliers de membres qui ont déjà transformé leur vie avec FitGang.',
                'date_modification': datetime.utcnow()
            }
        ]

        for item in default_content:
            op.execute(
                page_content_table.insert().values(
                    section=item['section'],
                    contenu=item['contenu'],
                    date_modification=item['date_modification']
                )
            )


def downgrade():
    # Only drop table if it exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'page_content' in existing_tables:
        op.drop_index('ix_page_content_section', table_name='page_content')
        op.drop_table('page_content')
