from rococo.data import MySqlAdapter
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv('.env.development')

def get_db_connection():
    
    host = os.get_env("MYSQL_HOST")
    port = int(os.get_env("MYSQL_PORT"))
    user = os.get_env("MYSQL_USER")
    password = os.get_env("MYSQL_PASSWORD")
    db = os.get_env("MYSQL_DATABASE")
    
    return MySqlAdapter(host=host, port=port, user=user, password=password, database=db)