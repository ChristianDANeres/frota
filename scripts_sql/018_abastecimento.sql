CREATE TABLE IF NOT EXISTS abastecimento (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER NOT NULL REFERENCES cliente(id),
    data            DATE NOT NULL,
    veiculo_id      INTEGER NOT NULL REFERENCES veiculo(id),
    km              NUMERIC(10,2) NOT NULL,
    quantidade      NUMERIC(10,3) NOT NULL,
    valor           NUMERIC(10,2) NOT NULL,
    motorista_id    INTEGER REFERENCES motorista(id),
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);
