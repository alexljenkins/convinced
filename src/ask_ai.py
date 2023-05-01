from typing import List, Dict, Literal, Tuple
import re

import openai

from src.message_log import (MessageLog,
                             TeacherResponse,
                             message_teacher_ai,
                             message_monster_ai,
                             wrap_message_monster_ai,
                             wrap_user_input,
                             parse_teacher_reponse)

PASSING_SCORE = 2200


def get_api_key(filepath:str) -> str:
    with open(filepath, "r") as txt_file:
        return txt_file.readlines()[0]


def ask_ai(user_input:str) ->Tuple[str, str]:
    key_filepath = ''
    key = get_api_key(key_filepath)

    teacher_response, teacher_log = ask_teacher_ai(user_input, key)
    parsed_teacher_response = parse_teacher_reponse(teacher_response)
    
    monster_response, monster_log = ask_monster_ai(user_input, parsed_teacher_response, key)
    
    return teacher_response, monster_response


def ask_teacher_ai(user_input:str, key:str) -> Tuple[str, MessageLog]:
    teacher_log = MessageLog()
    teacher_log.add_response("system", message_teacher_ai())
    teacher_log.add_response("user", wrap_user_input(user_input))
    
    teacher_ai = AI(key)
    success, response = teacher_ai.ask(teacher_log, temperature = 0.0)

    if success:
        teacher_log.add_response("assistant", response)

    return response, teacher_log


def ask_monster_ai(user_input:str, parsed_teacher_response:TeacherResponse, key:str) -> Tuple[str, MessageLog]:
    
    monster_log = MessageLog()
    monster_log.add_response("system", message_monster_ai(PASSING_SCORE))
    monster_log.add_response("user", wrap_message_monster_ai(parsed_teacher_response, user_input))
    
    monster_ai = AI(key)
    success, response = monster_ai.ask(monster_log, temperature = 0.3)
    
    if success:
        monster_log.add_response("assistant", response)

    return response, monster_log


class AI:
    def __init__(self, key:str, model:str = "gpt-3.5-turbo"):
        openai.api_key = key
        self.model = model

    def ask(self, message_log:MessageLog, temperature:float = 0.0) -> Tuple[bool, str]:
        try:
            response = openai.ChatCompletion.create(
                model = self.model,
                messages =  message_log,
                temperature = temperature, # explore vs exploit
            )
            text_response = response.choices[0].message["content"]
        except openai.error.RateLimitError as E:
            return False, "I'm too tired to deal with you today. Someone will have to pay me to keep listening to you..."
        except openai.error.InvalidRequestError as E:
            return False, "I have no idea what you're even talking about."
        except AttributeError as E:
            return False, "Oh no! My moving skill has stopped working... Too bad for you!"
        except Exception as E:
            return False, "Oh no! My brain has stopped working... Too bad for you!"
        
        return True, text_response
