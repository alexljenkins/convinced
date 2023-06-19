from typing import Tuple
import logging

import openai

from src.scenario.messages import MessageLog

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_api_key(filepath:str) -> str:
    with open(filepath, "r") as txt_file:
        return txt_file.readlines()[0]

class AI:
    def __init__(self, key:str, model:str = "gpt-3.5-turbo"):
        openai.api_key = key
        self.model = model

    def ask(self, message_log:MessageLog, temperature:float = 0.0) -> Tuple[bool, str]:
        try:
            response = openai.ChatCompletion.create(
                model = self.model,
                messages =  message_log.messages,
                temperature = temperature, # explore vs exploit
            )
            logging.info(response)
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
