from dotenv import load_dotenv
import sqlalchemy
import os 

if not load_dotenv(".env"):
    raise Exception("Envs are not loaded, check them please")

DBAPI = os.environ["DBAPI"]
DB = os.environ["DB"]

if DBAPI == 'sqlite':
    DB += '.db'
    # engine is great, extra abstraction layer - allows to interchange between sqlite3 and psql

Engine = sqlalchemy.create_engine(f"{DBAPI}://{DB}")