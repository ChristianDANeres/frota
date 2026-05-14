import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise SystemExit('DATABASE_URL not set')
# strip SQLAlchemy scheme if present
if DATABASE_URL.startswith('postgresql+psycopg2://'):
    url = DATABASE_URL.replace('postgresql+psycopg2://', 'postgresql://', 1)
else:
    url = DATABASE_URL
p = urlparse(url)
user = p.username
password = p.password
host = p.hostname or 'localhost'
port = p.port or 5432
dbname = p.path.lstrip('/')

sqls = [
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS endereco VARCHAR(255);",
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS municipio VARCHAR(120);",
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS responsavel VARCHAR(160);",
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS logo_esquerdo VARCHAR(255);",
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS logo_direito VARCHAR(255);",
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS email VARCHAR(160);",
    "ALTER TABLE cliente ADD COLUMN IF NOT EXISTS telefone VARCHAR(30);",
]

conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
conn.autocommit = True
cur = conn.cursor()
for s in sqls:
    try:
        cur.execute(s)
        print('OK:', s)
    except Exception as e:
        print('ERR:', s, e)
cur.close()
conn.close()
print('Done')
