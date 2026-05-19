from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text("UPDATE alembic_version SET version_num='0008_add_intercorrencia'"))
        conn.commit()
        r = conn.execute(text("SELECT version_num FROM alembic_version"))
        print("Versão atualizada para:", r.fetchall())
