CREATE TABLE IF NOT EXISTS usuario_perfil (
    usuario_id  INTEGER NOT NULL REFERENCES usuario(id),
    perfil_id   INTEGER NOT NULL REFERENCES perfil(id),
    PRIMARY KEY (usuario_id, perfil_id)
);
