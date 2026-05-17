"""adiciona coluna cpf em usuario

Revision ID: 0005_add_cpf_usuario
Revises: 0004_motivo_veiculo_oficina
Create Date: 2026-05-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '0005_add_cpf_usuario'
down_revision = '0004_motivo_veiculo_oficina'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if inspector.has_table('usuario'):
        cols = [c['name'] for c in inspector.get_columns('usuario')]
        if 'cpf' not in cols:
            op.add_column('usuario', sa.Column('cpf', sa.String(length=20), nullable=True))
            # criar constraint unique, protegido por try/except
            try:
                op.create_unique_constraint('uq_usuario_cpf', 'usuario', ['cpf'])
            except Exception:
                pass


def downgrade():
    # Não remover colunas automaticamente no downgrade para evitar perda de dados.
    pass
