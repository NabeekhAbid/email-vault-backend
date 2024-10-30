from rococo.data import MySqlAdapter
import os
from dotenv import load_dotenv
load_dotenv()
load_dotenv('.env.development')
def get_db_connection():
    host = os.getenv("MYSQL_HOST")
    port = int(os.getenv("MYSQL_PORT"))
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    db = os.getenv("MYSQL_DATABASE")
    return MySqlAdapter(host=host, port=port, user=user, password=password, database=db)