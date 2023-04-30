from typing import List, Dict, Literal
import re
from src.message_log import MessageLog


import openai


def get_api_key(filepath):
    with open(filepath, "r") as txt_file:
        return txt_file.readlines()[0]

def ask_ai(user_input):
    key_filepath = ''
    log = MessageLog()
    ai = AI(get_api_key(key_filepath), log)
    ai.set_responder("teacher")
    ai.log.add_response("user", user_input)
    
    success, response = ai.ask(user_input)
    
    if success:
        ai.log.add_response("assistant", user_input)


class AI:
    def __init__(self, key:str, message_log:MessageLog, model:str = "gpt-3.5-turbo"):
        openai.api_key = key
        self.model = model
        self.log = message_log
        
    def set_responder(self, role:Literal['monster', 'teacher']):
        if role not in ['monster', 'teacher']:
            raise ValueError("Role must be either 'monster' or 'teacher'")
        eval(f"self.log.set_{role}_ai()")

    def ask(self, temperature:float = 0.0):
        try:
            response = openai.ChatCompletion.create(
                model = self.model,
                messages = self.log,
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

    def ask_teacher(self, user_input:str):
        self.set_responder(role = 'teacher')
        self.log.add_response("user", self.log.wrap_user_input(user_input))
        return self.ask(temperature = 0.0)

    def ask_monster(self, user_input:str):
        self.set_responder(role = 'monster')
        self.log.add_response("user", self.log.wrap_user_input(user_input))
        return self.ask(temperature = 0.3)
