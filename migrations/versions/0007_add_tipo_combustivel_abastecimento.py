"""adiciona coluna tipo_combustivel em abastecimento

Revision ID: 0007_add_tipo_combustivel_abastecimento
Revises: 0006_add_uq_motorista_cnh
Create Date: 2026-05-17 00:00:00.000000
"""
from alembic import op

revision = '0007_add_tipo_combustivel_abastecimento'
down_revision = '0006_add_uq_motorista_cnh'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TABLE abastecimento
        ADD COLUMN IF NOT EXISTS tipo_combustivel VARCHAR(40)
    """)


def downgrade():
    op.execute("""
        ALTER TABLE abastecimento
        DROP COLUMN IF EXISTS tipo_combustivel
    """)
