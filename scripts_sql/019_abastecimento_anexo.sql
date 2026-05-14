CREATE TABLE IF NOT EXISTS abastecimento_anexo (
    id                  SERIAL PRIMARY KEY,
    cliente_id          INTEGER NOT NULL REFERENCES cliente(id),
    abastecimento_id    INTEGER NOT NULL REFERENCES abastecimento(id),
    tipo_arquivo_id     INTEGER REFERENCES tipo_arquivo(id),
    nome_arquivo        VARCHAR(255) NOT NULL,
    caminho_arquivo     VARCHAR(500) NOT NULL,
    tamanho_arquivo     INTEGER,
    criado_em           TIMESTAMP NOT NULL DEFAULT NOW()
);
