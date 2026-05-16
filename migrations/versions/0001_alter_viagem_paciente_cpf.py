"""alter viagem_paciente.cpf to varchar(20)

Revision ID: 0001_alter_viagem_paciente_cpf
Revises: 
Create Date: 2026-05-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_alter_viagem_paciente_cpf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # alter column cpf to length 20
    op.alter_column('viagem_paciente', 'cpf', existing_type=sa.VARCHAR(length=14), type_=sa.String(length=20), existing_nullable=False)


def downgrade():
    # revert column cpf back to length 14
    op.alter_column('viagem_paciente', 'cpf', existing_type=sa.VARCHAR(length=20), type_=sa.String(length=14), existing_nullable=False)
