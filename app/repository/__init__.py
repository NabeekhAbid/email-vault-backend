from rococo.repositories.mysql import MySqlRepository
from rococo.models.login_method import loginMethod
from ..db_connection import get_db_connection
from common.models.user_model import User


with get_db_connection() as adapter:
    user_repo = MySqlRepository(adapter, User, None)