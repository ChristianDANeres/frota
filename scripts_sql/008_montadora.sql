CREATE TABLE IF NOT EXISTS montadora (
    id          SERIAL PRIMARY KEY,
    cliente_id  INTEGER NOT NULL REFERENCES cliente(id),
    nome        VARCHAR(120) NOT NULL,
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_montadora_cliente_nome UNIQUE (cliente_id, nome)
);
