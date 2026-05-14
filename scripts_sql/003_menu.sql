CREATE TABLE IF NOT EXISTS menu (
    id          SERIAL PRIMARY KEY,
    cliente_id  INTEGER NOT NULL REFERENCES cliente(id),
    codigo      VARCHAR(60) NOT NULL,
    nome        VARCHAR(120) NOT NULL,
    icone       VARCHAR(60),
    endpoint    VARCHAR(120),
    ordem       INTEGER NOT NULL DEFAULT 0,
    menu_pai_id INTEGER REFERENCES menu(id),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_menu_cliente_codigo UNIQUE (cliente_id, codigo)
);
