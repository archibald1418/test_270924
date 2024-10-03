from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from pprint import pprint

#if not load_dotenv(".env", override=True):
#    raise Exception("Envs are not loaded, check them please")

DBAPI = os.environ["DBAPI"]
DB = os.environ["DB"]
DBURL = None

if DBAPI == 'sqlite':
    DB += '.db'
    DBURL = f"{DBAPI}:///{DB}"
elif 'pg' in DBAPI:
    PGUSER = os.environ['PGUSER']
    PGPASS = os.environ["PGPASS"]
    PGHOST = os.environ["PGHOST"]
    PGDB = os.environ["PGDB"]
    PGPORT = 5432

    DBURL=f'postgresql+{DBAPI}://{PGUSER}:{PGPASS}@{PGHOST}:5432/{PGDB}'

    # engine is great, extra abstraction layer - allows to interchange between sqlite3 and psql

# pprint(dict(os.environ.items()))

assert DBURL
Engine = sqlalchemy.create_engine(DBURL, echo=True)
Session = sessionmaker(Engine)
# session collects transactions and commits them at once
# also session can do queries (unlike connection)
