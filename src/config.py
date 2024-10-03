import os
from pprint import pprint

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

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


assert DBURL
Engine = sqlalchemy.create_engine(DBURL, echo=True)
Session = sessionmaker(Engine)
