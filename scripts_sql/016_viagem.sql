CREATE TYPE status_viagem_enum AS ENUM ('EM_ABERTO', 'INICIADA', 'FINALIZADA');

CREATE TABLE IF NOT EXISTS viagem (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER NOT NULL REFERENCES cliente(id),
    veiculo_id      INTEGER NOT NULL REFERENCES veiculo(id),
    motorista_id    INTEGER NOT NULL REFERENCES motorista(id),
    km_inicial      NUMERIC(10,2) NOT NULL,
    km_final        NUMERIC(10,2),
    destino         VARCHAR(255) NOT NULL,
    descricao       TEXT,
    status          status_viagem_enum NOT NULL DEFAULT 'EM_ABERTO',
    data_inicial    TIMESTAMP,
    data_final      TIMESTAMP,
    tipo_viagem_id  INTEGER REFERENCES tipo_viagem(id),
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);
