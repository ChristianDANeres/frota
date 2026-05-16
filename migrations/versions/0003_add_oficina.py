"""adiciona tabelas oficina e veiculo_oficina

Revision ID: 0003_add_oficina
Revises: 0002_cpf_11
Create Date: 2026-05-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '0003_add_oficina'
down_revision = '0002_cpf_11'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    # tabela oficina (cria somente se não existir)
    if not inspector.has_table('oficina'):
        op.create_table(
            'oficina',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('cliente_id', sa.Integer, sa.ForeignKey('cliente.id'), nullable=False),
            sa.Column('cnpj', sa.String(length=20), nullable=True),
            sa.Column('nome', sa.String(length=200), nullable=False),
            sa.Column('logradouro', sa.String(length=255), nullable=True),
            sa.Column('numero', sa.String(length=50), nullable=True),
            sa.Column('municipio', sa.String(length=120), nullable=True),
            sa.Column('estado', sa.String(length=2), nullable=True),
            sa.Column('email', sa.String(length=200), nullable=True),
            sa.Column('telefone', sa.String(length=50), nullable=True),
            sa.Column('responsavel', sa.String(length=160), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
            sa.Column('atualizado_em', sa.DateTime(), nullable=False),
        )
        try:
            op.create_index(op.f('ix_oficina_cliente_id'), 'oficina', ['cliente_id'], unique=False)
        except Exception:
            pass

    # tabela veiculo_oficina (cria somente se não existir)
    if not inspector.has_table('veiculo_oficina'):
        op.create_table(
            'veiculo_oficina',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('cliente_id', sa.Integer, sa.ForeignKey('cliente.id'), nullable=False),
            sa.Column('oficina_id', sa.Integer, sa.ForeignKey('oficina.id'), nullable=False),
            sa.Column('veiculo_id', sa.Integer, sa.ForeignKey('veiculo.id'), nullable=False),
            sa.Column('data_entrada', sa.DateTime(), nullable=False),
            sa.Column('data_saida', sa.DateTime(), nullable=True),
            sa.Column('km_entrada', sa.Numeric(10, 2), nullable=True),
            sa.Column('km_saida', sa.Numeric(10, 2), nullable=True),
            sa.Column('motorista_entrada_id', sa.Integer, sa.ForeignKey('motorista.id'), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
            sa.Column('atualizado_em', sa.DateTime(), nullable=False),
        )
        try:
            op.create_index(op.f('ix_veiculo_oficina_cliente_id'), 'veiculo_oficina', ['cliente_id'], unique=False)
        except Exception:
            pass

    # tabela veiculo_oficina_anexo (cria somente se não existir)
    if not inspector.has_table('veiculo_oficina_anexo'):
        op.create_table(
            'veiculo_oficina_anexo',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('cliente_id', sa.Integer, sa.ForeignKey('cliente.id'), nullable=False),
            sa.Column('veiculo_oficina_id', sa.Integer, sa.ForeignKey('veiculo_oficina.id'), nullable=False),
            sa.Column('tipo_arquivo_id', sa.Integer, sa.ForeignKey('tipo_arquivo.id'), nullable=True),
            sa.Column('nome_arquivo', sa.String(length=255), nullable=False),
            sa.Column('caminho_arquivo', sa.String(length=500), nullable=False),
            sa.Column('tamanho_arquivo', sa.Integer(), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
        )
        try:
            op.create_index(op.f('ix_veiculo_oficina_anexo_cliente_id'), 'veiculo_oficina_anexo', ['cliente_id'], unique=False)
        except Exception:
            pass


def downgrade():
    # Não remover tabelas no downgrade para evitar perda de dados.
    # Downgrade intencionalmente é no-op; alterações de reversão devem ser feitas manualmente se necessário.
    pass
