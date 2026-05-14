CREATE TABLE IF NOT EXISTS veiculo (
    id                  SERIAL PRIMARY KEY,
    cliente_id          INTEGER NOT NULL REFERENCES cliente(id),
    placa               VARCHAR(10) NOT NULL,
    montadora_id        INTEGER REFERENCES montadora(id),
    modelo              VARCHAR(120),
    cor_id              INTEGER REFERENCES cor(id),
    ano_fabricacao      INTEGER,
    tipo_combustivel    VARCHAR(40),
    status_veiculo_id   INTEGER REFERENCES status_veiculo(id),
    ativo               BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em           TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_veiculo_cliente_placa UNIQUE (cliente_id, placa)
);
