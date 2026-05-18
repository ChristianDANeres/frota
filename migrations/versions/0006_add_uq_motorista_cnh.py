"""adiciona unique constraint de CNH em motorista

Revision ID: 0006_add_uq_motorista_cnh
Revises: 0005_add_cpf_usuario
Create Date: 2026-05-17 00:00:00.000000
"""
from alembic import op

revision = '0006_add_uq_motorista_cnh'
down_revision = '0005_add_cpf_usuario'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TABLE motorista
        ADD CONSTRAINT uq_motorista_cliente_cnh UNIQUE (cliente_id, cnh)
    """)


def downgrade():
    op.execute("""
        ALTER TABLE motorista
        DROP CONSTRAINT IF EXISTS uq_motorista_cliente_cnh
    """)
