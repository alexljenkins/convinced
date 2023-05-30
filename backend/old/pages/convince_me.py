
from typing import Literal
from app.api.database import save_entry, check_entry_against_db, update_entry_with_teacher, update_entry_with_character
from app.api.elo import starting_elo
from app.ask_ai import ask_teacher_ai, ask_character_ai
from app.api.message_log import parse_teacher_reponse


def too_short_validation(user_input) -> bool:
    word_count = len(user_input.split())
    return word_count < 10

def too_long_validation(user_input) -> bool:
    word_count = len(user_input.split())
    return word_count > 200


def check_user_input(db, user_input):
    if too_short_validation(user_input):
        return "Your answer is too short. Please write at least 10 words and no more than 200 words.", False
    
    if too_long_validation(user_input):
        return "Your answer is too long. Please write at least 10 words and no more than 200 words.", False
    
    return False, True


def teacher_ai(user_input):
    response, passed = check_user_input(db, user_input, 'teacher')

    if not passed:
        return response, False
    
    existing_teacher_response, existing_character_response = check_entry_against_db(db, user_input)
    if isinstance(existing_teacher_response, str) and existing_teacher_response:
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
