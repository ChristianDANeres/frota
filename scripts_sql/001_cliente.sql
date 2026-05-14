CREATE TABLE IF NOT EXISTS cliente (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(160) NOT NULL UNIQUE,
    cnpj        VARCHAR(20),
    email       VARCHAR(160),
    telefone    VARCHAR(30),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);
