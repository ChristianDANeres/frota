CREATE TABLE IF NOT EXISTS perfil_menu (
    perfil_id   INTEGER NOT NULL REFERENCES perfil(id),
    menu_id     INTEGER NOT NULL REFERENCES menu(id),
    PRIMARY KEY (perfil_id, menu_id)
);
