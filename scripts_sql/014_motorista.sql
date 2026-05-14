CREATE TABLE IF NOT EXISTS motorista (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER NOT NULL REFERENCES cliente(id),
    cpf             VARCHAR(14) NOT NULL,
    nome            VARCHAR(160) NOT NULL,
    data_nascimento DATE,
    cnh             VARCHAR(20) NOT NULL,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_motorista_cliente_cpf UNIQUE (cliente_id, cpf)
);
