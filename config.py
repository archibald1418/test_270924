from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from pprint import pprint

if not load_dotenv(".env", override=True):
    raise Exception("Envs are not loaded, check them please")

DBAPI = os.environ["DBAPI"]
DB = os.environ["DB"]
DBURL = None

if DBAPI == 'sqlite':
    DB += '.db'
    DBURL = f"{DBAPI}:///{DB}"
    print(DBAPI)
elif 'pg' in DBAPI:
    PGUSER = os.environ['PGUSER']
    PGPASSWORD = os.environ["PGPASSWORD"]
    PGHOST = os.environ["PGHOST"]
    PGPORT = os.environ["PGPORT"]
    
    DBURL = f'postgresql+{DBAPI}://{PGUSER}@{PGHOST}:{PGPORT}/{DB}'

    # engine is great, extra abstraction layer - allows to interchange between sqlite3 and psql

print(DBURL)
# pprint(dict(os.environ.items()))


Engine = sqlalchemy.create_engine(DBURL, echo=True)
Session = sessionmaker(Engine)
# session collects transactions and commits them at once
# also session can do queries (unlike connection)