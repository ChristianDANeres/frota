-- =============================================================================
-- 020 – Menus: Diário e Intercorrência
-- Insere os menus para todos os clientes existentes e associa aos perfis ativos.
-- Execute em produção ANTES de fazer deploy da versão que contém essas rotas.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Inserir menu Diário (se ainda não existir para o cliente)
-- -----------------------------------------------------------------------------
INSERT INTO menu (cliente_id, codigo, nome, icone, endpoint, ordem, menu_pai_id, ativo)
SELECT
    c.id,
    'diario',
    'Diário',
    'bi-journal-text',
    'diario.listar',
    70,
    NULL,
    TRUE
FROM cliente c
WHERE NOT EXISTS (
    SELECT 1
    FROM   menu m
    WHERE  m.cliente_id = c.id
    AND    m.codigo     = 'diario'
);

-- -----------------------------------------------------------------------------
-- 2. Inserir menu Intercorrência (se ainda não existir para o cliente)
-- -----------------------------------------------------------------------------
INSERT INTO menu (cliente_id, codigo, nome, icone, endpoint, ordem, menu_pai_id, ativo)
SELECT
    c.id,
    'intercorrencia',
    'Intercorrências',
    'bi-exclamation-triangle',
    'intercorrencia.listar',
    80,
    NULL,
    TRUE
FROM cliente c
WHERE NOT EXISTS (
    SELECT 1
    FROM   menu m
    WHERE  m.cliente_id = c.id
    AND    m.codigo     = 'intercorrencia'
);

-- -----------------------------------------------------------------------------
-- 3. Associar menu Diário a todos os perfis ativos de cada cliente
--    (pula duplicatas com ON CONFLICT DO NOTHING)
-- -----------------------------------------------------------------------------
INSERT INTO perfil_menu (perfil_id, menu_id)
SELECT
    p.id  AS perfil_id,
    m.id  AS menu_id
FROM   menu    m
JOIN   perfil  p  ON p.cliente_id = m.cliente_id
                  AND p.ativo     = TRUE
WHERE  m.codigo = 'diario'
ON CONFLICT DO NOTHING;

-- -----------------------------------------------------------------------------
-- 4. Associar menu Intercorrência a todos os perfis ativos de cada cliente
-- -----------------------------------------------------------------------------
INSERT INTO perfil_menu (perfil_id, menu_id)
SELECT
    p.id  AS perfil_id,
    m.id  AS menu_id
FROM   menu    m
JOIN   perfil  p  ON p.cliente_id = m.cliente_id
                  AND p.ativo     = TRUE
WHERE  m.codigo = 'intercorrencia'
ON CONFLICT DO NOTHING;

-- -----------------------------------------------------------------------------
-- 5. Verificação rápida após execução
-- -----------------------------------------------------------------------------
SELECT
    c.nome                    AS cliente,
    m.codigo,
    m.nome                    AS menu_nome,
    m.icone,
    m.endpoint,
    m.ordem,
    COUNT(pm.perfil_id)       AS perfis_vinculados
FROM   menu          m
JOIN   cliente       c  ON c.id       = m.cliente_id
LEFT   JOIN perfil_menu pm ON pm.menu_id = m.id
WHERE  m.codigo IN ('diario', 'intercorrencia')
GROUP  BY c.nome, m.codigo, m.nome, m.icone, m.endpoint, m.ordem
ORDER  BY c.nome, m.ordem;
