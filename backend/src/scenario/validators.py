from typing import Tuple

def too_short_validation(user_input) -> bool:
    word_count = len(user_input.split())
    return word_count < 10

def too_long_validation(user_input) -> bool:
    word_count = len(user_input.split())
    return word_count > 200


def check_user_input(user_input) -> Tuple[str, bool]:
    if too_short_validation(user_input):
        return "Your answer is too short. Please write at least 10 words and no more than 200 words.", False
    
    if too_long_validation(user_input):
        return "Your answer is too long. Please write at least 10 words and no more than 200 words.", False
    
    return '', True

