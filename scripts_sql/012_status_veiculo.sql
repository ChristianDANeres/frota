CREATE TABLE IF NOT EXISTS status_veiculo (
    id          SERIAL PRIMARY KEY,
    cliente_id  INTEGER NOT NULL REFERENCES cliente(id),
    nome        VARCHAR(80) NOT NULL,
    descricao   VARCHAR(255),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_status_veiculo_cliente_nome UNIQUE (cliente_id, nome)
);
