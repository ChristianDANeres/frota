CREATE TABLE IF NOT EXISTS usuario (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(80) NOT NULL UNIQUE,
    nome        VARCHAR(160) NOT NULL,
    email       VARCHAR(160),
    telefone    VARCHAR(30),
    senha_hash  VARCHAR(255) NOT NULL,
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    is_admin    BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);
