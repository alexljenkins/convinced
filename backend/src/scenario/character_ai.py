from typing import Tuple
import logging

from src.scenario.validators import check_user_input
from src.scenario.messages import MessageLog, preface_character_ai_message, wrap_user_input
from src.database.database_calls import check_entry_against_db, save_entry
from src.database.entries import Entry
from src.globals import DATABASE, CHARACTER_AI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def ask_character_ai(user_input:str) -> Tuple[str, bool]:
    user_error_response, passed = check_user_input(user_input)

    if not passed:
        return user_error_response, False

    existing_character_response = check_entry_against_db(DATABASE, user_input)
    if isinstance(existing_character_response, str) and existing_character_response:
        logger.info(f"Response already exists in database.")
        return existing_character_response, False
    
    # if all checks pass, ask AI for a response
    character_log = MessageLog()
    character_log.add_response("system", preface_character_ai_message())
    character_log.add_response("user", wrap_user_input(user_input))
    
    logger.info(f"Monster Log:\n{character_log.messages}")
    
    success, response = CHARACTER_AI.ask(character_log, temperature = 0.3)
    
    if isinstance(response, str) and response and success:
        new_entry = Entry(user_input = user_input, character_response = response)
        logger.info(f"Saving entry to database.")
        save_entry(DATABASE, new_entry)

    return response, success
