import re
import json
from pydantic.dataclasses import dataclass

PASSING_SCORE = 2200


class MessageLog:
    def __init__(self):
        self.messages = [{}]
    
    def add_response(self, role:str, content:str):
        self.messages.append({"role": role, "content": content})
    
    def set_teacher_ai(self):
        self.messages.append({
            "role":"system",
            "content":re.sub(' +', ' ',
                """You are an english teacher and have to give specific, actionable feedback to users' writing based on the topic:
                ```TOPIC: You are stopped by a monster guarding a bridge, you have to convince the monster to let you past, what would you say?```
                Use the following marking criteria:
                ``` MARKING CRITERIA:
                    1: Believability - how believable the user's story would be to the monster, given the scenario.
                    2: Engagement - how well the user's writing hooks the reader.
                    3. Relevence - how well the user's writing makes sense given the scenario.
                    ```
                As a teacher you do not tolerate any abusive language, so if the user uses any abusive language, you should give them a score of 0.
                Your response needs to be in the following json/dict format:
                {
                    'OVERALL_SCORE': <int out of 3000 based on the marking criteria>,
                    'BELIEVABILITY': {
                        'SCORE': <int out of 1000>,
                        'FEEDBACK': <str with specific, actionable feedback to improve believability. Do not create any examples.>,},
                    'ENGAGEMENT': {
                        'SCORE': <int out of 1000>,
                        'FEEDBACK': <str with specific, actionable feedback to improve engagement. Do not create any examples.>,},
                    'RELEVENCE': {
                        'SCORE': <int out of 1000>,
                        'FEEDBACK': <str with specific, actionable feedback to improve relevence. Do not create any examples.>,},
                }
            """)
        })

    def shorten_teacher_ai_for_monster(self):
        self.messages[0] = ({
            "role":"system",
            "content":re.sub(' +', ' ',
                """A teacher has marked a student's work and have to give specific, actionable feedback to users' writing based on the topic:
                ```TOPIC: You are stopped by a monster guarding a bridge, you have to convince the monster to let you past, what would you say?```
                Use the following marking criteria:
                ``` MARKING CRITERIA:
                    1: Believability - how believable the user's story would be to the monster, given the scenario.
                    2: Engagement - how well the user's writing hooks the reader.
                    3. Relevence - how well the user's writing makes sense given the scenario.
                    ```
                As a teacher you do not tolerate any abusive language, so if the user uses any abusive language, you should give them a score of 0.
                Your response needs to be in the following json/dict format:
                {
                    'OVERALL_SCORE': <int out of 3000 based on the marking criteria>,
                    'BELIEVABILITY': {
                        'SCORE': <int out of 1000>,
                        'FEEDBACK': <str with specific, actionable feedback to improve believability. Do not create any examples.>,},
                    'ENGAGEMENT': {
                        'SCORE': <int out of 1000>,
                        'FEEDBACK': <str with specific, actionable feedback to improve engagement. Do not create any examples.>,},
                    'RELEVENCE': {
                        'SCORE': <int out of 1000>,
                        'FEEDBACK': <str with specific, actionable feedback to improve relevence. Do not create any examples.>,},
                }
            """)
        })
        
    def set_monster_ai(self):
        self.messages.append({
            "role":"system",
            "content":re.sub(' +', ' ',
                f"""You are a monster guarding a bridge. Your job is to not let anyone past unless their 'OVERALL_SCORE' is above {PASSING_SCORE}.
                If their score is over {PASSING_SCORE}, write a response as the monster, acknowledge the adventure's (user's) specific need to cross and praising their story.
                However, if their score is below {PASSING_SCORE}, write a response as the monster that makes fun of their attempt, the lower the score - the harsher your response should be.
                You should not mention the score, marking criteria, the teacher or feedback in your response as you should be in character as the monster.
                You should reference specific things from the user's story in your response as proof you've listened.
                Do not break character, do not use vulgar language.
            """)
        })
    
    def wrap_user_input(self, user_input:str):
        return f"""``` USER WROTE AS THE ADVENTURER:
        {user_input}```"""
    
    def parse_teacher_reponse(self, text:str):
        brace_idx = text.find('{')
        if not brace_idx == -1:
            text = text[brace_idx:]
        
        brace_idx = text.rfind('}')
        if not brace_idx == -1:
            text = text[:brace_idx+1]
        
        try:
            _ = json.loads(text)
        except Exception as E:
            return False, text
        return True, text

    def log_teacher_response(self, response):
        success, dictionary = self.parse_teacher_reponse(response)
        
        if not success:
            return False, dictionary
        
        self.messages.append({"role":"assistant", "content":str(dictionary)})
        
        return True, dictionary






@dataclass
class Criteria:
    SCORE: int
    FEEDBACK: str


@dataclass
class TeacherResponse:
    OVERALL_SCORE: int
    BELIEVABILITY: Criteria
    ENGAGEMENT: Criteria
    RELEVENCE: Criteria