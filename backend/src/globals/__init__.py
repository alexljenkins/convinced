from database.database_calls import db_connect
from scenario.gpt_api import AI


DATABASE = db_connect()
CHARACTER_AI = AI()
