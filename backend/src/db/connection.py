import sqlite3
from sqlite3 import connect, Row

from src.config import env, DB_PREFIX, get_logger

logger = get_logger()

def db_url_to_name(dbt_url: str): 
    return dbt_url.removeprefix(DB_PREFIX)

# TODO use a connection pool
def make_connection(database_name):
    sqlite3.threadsafety = 3
    conn = connect(
        database_name, 
        autocommit = False, 
        check_same_thread = False,
        detect_types = sqlite3.PARSE_DECLTYPES,
    )
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = Row
    conn.commit()
    return conn

def default_db_connection(): 
    conn_str = db_url_to_name(env.database_url)
    return make_connection(conn_str)


