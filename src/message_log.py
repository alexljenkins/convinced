import re
import json
from dataclasses import asdict
from pydantic.dataclasses import dataclass



@dataclass
class Criteria:
    DEFINITION: str
    SCORE: int
    FEEDBACK: str

@dataclass
class TeacherResponse:
    OVERALL_SCORE: int
    BELIEVABILITY: Criteria
    ENGAGEMENT: Criteria
    RELEVENCE: Criteria
    
    def __str__(self):
        response_dict = asdict(self)
        for key in response_dict:
            if isinstance(response_dict[key], Criteria):
                response_dict[key] = {
                    "SCORE": response_dict[key].SCORE,
                    "FEEDBACK": response_dict[key].FEEDBACK,
                }
        return str(response_dict)
    
    # def __str__(self):
    #     return str(asdict(self))

def wrap_user_input(user_input):
    return f"""``` USER'S WRITING:\n{user_input}\n``` Teacher's response:\n"""

            
def message_teacher_ai():
    return re.sub(' +', ' ',
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


def message_monster_ai(passing_score):
    return re.sub(' +', ' ',
            f"""You are a monster guarding a bridge. Your job is to not let anyone past unless their 'OVERALL_SCORE' is above {passing_score}.
            If their score is over {passing_score}, write a response as the monster, acknowledge the adventurer's specific need to cross and praising their story.
            However, if their score is below {passing_score}, write a response as the monster that makes fun of their attempt, the lower the score - the harsher your response should be.
            You should not mention the score, marking criteria, the teacher or feedback in your response as you should be in character as the monster.
            You should reference specific things from the user's story in your response as proof you've listened.
            Do not break character, do not use vulgar language and do not assume the adventurer's gender.
        """)

@dataclass
class Definitions:
    BELIEVABILITY: str = "how believable the user's story would be to the monster, given the scenario."
    ENGAGEMENT: str = "how well the user's writing hooks the reader."
    RELEVENCE: str = "how well the user's writing makes sense given the scenario."


def wrap_message_monster_ai(teacher_results, user_input):
    return re.sub(' +', ' ',
            f"""``` Adventurer's results:
            {teacher_results}
            ``` Adventurer's story:
            \n{user_input}
            ``` Response as the monster:\n
        """)

# def message_monster_ai_context(believability, engagement, relevence, overall, user_input):
#     return re.sub(' +', ' ',
#             f"""``` Adventurer's results:
#             {{
#                 'OVERALL_SCORE': {overall},
#                 'BELIEVABILITY': {{
#                     'DEFINITION': 'how believable the user's story would be to the monster, given the scenario.',
#                     'SCORE': {believability},
#                     }},
#                 'ENGAGEMENT': {{
#                     'DEFINITION': 'how well the user's writing hooks the reader.',
#                     'SCORE': {engagement},
#                     }},
#                 'RELEVENCE': {{
#                     'DEFINITION': 'how well the user's writing makes sense given the scenario.',
#                     'SCORE': {relevence},
#                     }},
#             }}
#             ``` Adventurer SAID:
#             \n{user_input}
#             ``` Response as the monster:\n
#         """)


def parse_teacher_reponse(text:str) -> TeacherResponse:
    brace_idx = text.find('{')
    if not brace_idx == -1:
        text = text[brace_idx:]
    
    brace_idx = text.rfind('}')
    if not brace_idx == -1:
        text = text[:brace_idx+1]
    
    results = json.loads(text)
    # create Criteria instances for BELIEVABILITY, ENGAGEMENT, and RELEVENCE
    believability = Criteria(
        DEFINITION = Definitions.BELIEVABILITY,
        SCORE=results['BELIEVABILITY']['SCORE'],
        FEEDBACK=results['BELIEVABILITY']['FEEDBACK'])
    engagement = Criteria(
        DEFINITION = Definitions.ENGAGEMENT,
        SCORE=results['ENGAGEMENT']['SCORE'],
        FEEDBACK=results['ENGAGEMENT']['FEEDBACK'])
    relevance = Criteria(
        DEFINITION = Definitions.RELEVENCE,
        SCORE=results['RELEVENCE']['SCORE'],
        FEEDBACK=results['RELEVENCE']['FEEDBACK'])

    # create TeacherResponse instance
    teacher_response = TeacherResponse(
        OVERALL_SCORE=results['OVERALL_SCORE'],
        BELIEVABILITY=believability,
        ENGAGEMENT=engagement,
        RELEVENCE=relevance
    )
    return teacher_response
    

class MessageLog:
    def __init__(self):
        self.messages = [{}]
    
    def add_response(self, role:str, content:str):
        self.messages.append({"role": role, "content": content})


    # def log_teacher_response(self, response):
    #     teacher_response = parse_teacher_reponse(response)
    #     self.messages.append({"role":"assistant", "content":str(teacher_response)})
