from typing import Tuple
import logging

from app.scenario.validators import check_user_input

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


def teacher_ai(user_input):

    response, passed = check_user_input(user_input)

    if not passed:
        return response, False
    
    existing_teacher_response, existing_character_response = check_entry_against_db(db, user_input)
    
    if isinstance(existing_teacher_response, str):
        existing_teacher_response_parsed = parse_teacher_reponse(existing_teacher_response)
        return existing_teacher_response_parsed, False


    # if all checks pass, ask AI for a response
    teacher_response, teacher_log = ask_teacher_ai(user_input, key)
    parsed_teacher_response = parse_teacher_reponse(teacher_response)
    
    if isinstance(existing_character_response, str) and existing_character_response:
        update_entry_with_teacher(db, user_input, parsed_teacher_response.__str__())
    else:
        save_entry(db, user_input, parsed_teacher_response.__str__(), None, starting_elo())
        
    return parsed_teacher_response, True


def ask_teacher_ai(user_input:str, key:str) -> Tuple[str, MessageLog]:
    teacher_log = MessageLog()
    teacher_log.add_response("system", message_teacher_ai())
    teacher_log.add_response("user", wrap_user_input(user_input))
    
    teacher_ai = AI(key)
    success, response = teacher_ai.ask(teacher_log, temperature = 0.1)

    if success:
        logger.info(f"Adding AI response to teacher log.")
        teacher_log.add_response("assistant", response)

    return response, teacher_log

