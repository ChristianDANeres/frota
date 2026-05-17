import psycopg2

conn = psycopg2.connect(
    host='localhost', port=5432,
    user='postgres', password='pgpgpg', dbname='frota'
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("ALTER TABLE usuario ADD COLUMN IF NOT EXISTS cpf VARCHAR(20);")
print("OK: coluna cpf adicionada")

try:
    cur.execute("ALTER TABLE usuario ADD CONSTRAINT uq_usuario_cpf UNIQUE (cpf);")
    print("OK: constraint UNIQUE adicionada")
except Exception as e:
    print("AVISO (provavelmente já existe):", e)

cur.close()
conn.close()
print("Pronto!")
