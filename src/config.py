import os
from pprint import pprint

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.engine import Engine

#if not load_dotenv(".env", override=True):
#    raise Exception("Envs are not loaded, check them please")

def get_dburl() -> str:
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
        PGPORT = os.environ.get("PGPORT") or 5432

        DBURL=f'postgresql+{DBAPI}://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGDB}'

    assert DBURL

    return DBURL

def get_engine() -> Engine:
    return sqlalchemy.create_engine(get_dburl(), echo=True)
