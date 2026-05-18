import psycopg2

conn = psycopg2.connect('postgresql://postgres:pgpgpg@localhost:5432/frota')
cur = conn.cursor()
cur.execute("ALTER TABLE motorista ADD CONSTRAINT uq_motorista_cliente_cnh UNIQUE (cliente_id, cnh)")
conn.commit()
cur.close()
conn.close()
print('OK: constraint uq_motorista_cliente_cnh adicionada')
