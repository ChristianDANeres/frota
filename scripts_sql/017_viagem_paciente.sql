CREATE TABLE IF NOT EXISTS viagem_paciente (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER NOT NULL REFERENCES cliente(id),
    viagem_id       INTEGER NOT NULL REFERENCES viagem(id),
    cpf             VARCHAR(14) NOT NULL,
    nome            VARCHAR(160) NOT NULL,
    nome_mae        VARCHAR(160) NOT NULL,
    data_nascimento DATE NOT NULL,
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW()
);
