"""adiciona coluna motivo em veiculo_oficina

Revision ID: 0004_add_motivo_veiculo_oficina
Revises: 0003_add_oficina
Create Date: 2026-05-15 00:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '0004_motivo_veiculo_oficina'
down_revision = '0003_add_oficina'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if inspector.has_table('veiculo_oficina'):
        cols = [c['name'] for c in inspector.get_columns('veiculo_oficina')]
        if 'motivo' not in cols:
            op.add_column('veiculo_oficina', sa.Column('motivo', sa.String(length=4000), nullable=True))


def downgrade():
    # Não remover colunas automaticamente no downgrade para evitar perda de dados.
    pass
