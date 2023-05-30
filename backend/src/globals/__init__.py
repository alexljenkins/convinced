from src.database.database_calls import db_connect
from src.scenario.gpt_api import get_api_key, AI


DATABASE = db_connect()
CHARACTER_AI = AI(get_api_key('api_key'))
