"""alter viagem_paciente.cpf to varchar(11)

Revision ID: 0002_alter_viagem_paciente_cpf_11
Revises: 0001_alter_viagem_paciente_cpf
Create Date: 2026-05-14 00:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_cpf_11'
down_revision = '0001_alter_viagem_paciente_cpf'
branch_labels = None
depends_on = None


def upgrade():
    # limpar dados existentes: manter apenas dígitos e truncar para 11
    op.execute("""
        UPDATE viagem_paciente
        SET cpf = substring(regexp_replace(cpf, '\\D', '', 'g') from 1 for 11)
    """)
    op.alter_column('viagem_paciente', 'cpf', existing_type=sa.VARCHAR(length=20), type_=sa.String(length=11), existing_nullable=False)


def downgrade():
    op.alter_column('viagem_paciente', 'cpf', existing_type=sa.VARCHAR(length=11), type_=sa.String(length=20), existing_nullable=False)
