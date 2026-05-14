CREATE TABLE IF NOT EXISTS usuario_cliente (
    usuario_id  INTEGER NOT NULL REFERENCES usuario(id),
    cliente_id  INTEGER NOT NULL REFERENCES cliente(id),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (usuario_id, cliente_id)
);
