"""adiciona tabela intercorrencia

Revision ID: 0008_add_intercorrencia
Revises: 0007_add_tipo_combustivel_abastecimento
Create Date: 2026-05-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0008_add_intercorrencia'
down_revision = '0007_add_tipo_combustivel_abastecimento'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS intercorrencia (
            id                          SERIAL PRIMARY KEY,
            cliente_id                  INTEGER NOT NULL REFERENCES cliente(id),
            viagem_id                   INTEGER NOT NULL REFERENCES viagem(id),
            viagem_paciente_id          INTEGER REFERENCES viagem_paciente(id),
            local_origem                VARCHAR(255) NOT NULL,
            local_destino               VARCHAR(255),
            data_transporte             DATE NOT NULL,
            horario_ocorrencia          TIME NOT NULL,
            paciente_nome               VARCHAR(160) NOT NULL,
            paciente_idade              INTEGER,
            paciente_telefone           VARCHAR(20),
            paciente_acompanhante       VARCHAR(160),
            cond_deambula               BOOLEAN NOT NULL DEFAULT FALSE,
            cond_nao_deambula           BOOLEAN NOT NULL DEFAULT FALSE,
            cond_acamado                BOOLEAN NOT NULL DEFAULT FALSE,
            cond_cadeirante             BOOLEAN NOT NULL DEFAULT FALSE,
            cond_dispositivo_mobil      BOOLEAN NOT NULL DEFAULT FALSE,
            cond_traqueostomizado       BOOLEAN NOT NULL DEFAULT FALSE,
            cond_oxigenio_continuo      BOOLEAN NOT NULL DEFAULT FALSE,
            cond_portador_ostomias      BOOLEAN NOT NULL DEFAULT FALSE,
            cond_drenos_dispositivos    BOOLEAN NOT NULL DEFAULT FALSE,
            cond_acesso_venoso_periferico BOOLEAN NOT NULL DEFAULT FALSE,
            cond_acesso_venoso_central  BOOLEAN NOT NULL DEFAULT FALSE,
            descricao_ocorrencia        TEXT,
            endereco_ocorrencia         VARCHAR(500),
            socorristas                 VARCHAR(500),
            destino_usuario             VARCHAR(20),
            data_atendimento            DATE,
            local_atendimento           VARCHAR(255),
            observacoes                 TEXT,
            status                      VARCHAR(20) NOT NULL DEFAULT 'EM_ABERTO',
            criado_em                   TIMESTAMP NOT NULL DEFAULT NOW(),
            atualizado_em               TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_intercorrencia_cliente_id ON intercorrencia(cliente_id)")


def downgrade():
    op.execute("DROP TABLE IF EXISTS intercorrencia")
