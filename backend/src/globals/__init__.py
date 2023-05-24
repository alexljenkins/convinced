from database.database_calls import db_connect
from scenario.gpt_api import get_api_key, AI


DATABASE = db_connect()
STARTING_ELO = 1200
CHARACTER_AI = AI(get_api_key('api_key'))
