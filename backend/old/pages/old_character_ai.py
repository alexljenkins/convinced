from typing import Tuple
import logging

from app.review.elo import starting_elo
from app.scenario.gpt_api import AI
from app.scenario.messages import (MessageLog,
                             TeacherResponse,
                             message_teacher_ai,
                             message_monster_ai_not_passing,
                             message_monster_ai_passing,
                             wrap_message_monster_ai,
                             wrap_user_input,
                             parse_teacher_reponse)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

PASSING_SCORE = 2200

def character_ai(user_input, scores):
    response, passed = check_user_input(db, user_input, 'character')

    if not passed:
        return response, False
    
    existing_teacher_response, existing_character_response = check_entry_against_db(db, user_input)
    if isinstance(existing_character_response, str) and existing_character_response:
        return existing_character_response, False
    
    # if all checks pass, ask AI for a response
    character_response, character_log = ask_character_ai(user_input, scores, key)
    
    if isinstance(existing_teacher_response, str) and existing_teacher_response:
        update_entry_with_character(db, user_input, character_response)
    else:
        save_entry(db, user_input, None, character_response, starting_elo())
    
    return character_response, True


def ask_character_ai(user_input:str, parsed_teacher_response:TeacherResponse, key:str) -> Tuple[str, MessageLog]:
    monster_log = MessageLog()
    if parsed_teacher_response.OVERALL.SCORE >= PASSING_SCORE:
        monster_log.add_response("system", message_monster_ai_passing())
    else:  # do not let them past
        lowest_criterion = parsed_teacher_response.get_lowest_score_criterion()
        harshness_degree = lowest_criterion.get_harshness_degree()
        monster_log.add_response("system", message_monster_ai_not_passing(lowest_criterion.NAME, harshness_degree))
    
    monster_log.add_response("user", wrap_message_monster_ai(user_input))
    logger.info(f"Monster Log:\n{monster_log.messages}")
    monster_ai = AI(key)
    success, response = monster_ai.ask(monster_log, temperature = 0.3)
    
    if success:
        monster_log.add_response("assistant", response)

    return response, monster_log
