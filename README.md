# FROTA

Projeto Flask multi-tenant com banco único PostgreSQL.

## Estrutura

- `app/auth`: login e logout
- `app/cliente`: seleção do cliente/tenant na sessão
- `app/security`: base de usuários, perfis, menus e clientes
- `app/frota`: módulo inicial do sistema FROTA
- `app/models.py`: modelos centrais com `cliente_id` nas tabelas de negócio
- `app/templates`: templates separados por módulo

## Rodar local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask --app run.py db init
flask --app run.py db migrate -m "estrutura inicial"
flask --app run.py db upgrade
python run.py
```

O projeto também cria as tabelas automaticamente no primeiro boot via `db.create_all()`.

Login inicial:

- Usuário: `admin`
- Senha: `admin123`

## Multi-tenant

O banco é único PostgreSQL. A separação dos dados acontece pelo campo `cliente_id`. Todo módulo de negócio deve herdar `TenantMixin` ou declarar explicitamente `cliente_id`.
