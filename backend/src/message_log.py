import re
import json
import logging
from dataclasses import asdict
from pydantic.dataclasses import dataclass
import pandas as pd
logger = logging.getLogger(__name__)


@dataclass
class Criteria:
    NAME: str
    DEFINITION: str
    SCORE: int
    FEEDBACK: str

    def display_format(self):
        return f"  \n\t\tFeedback: {self.FEEDBACK}  \n\t\tScore: {self.SCORE}  \n"
    
    def df_format(self):
        return pd.DataFrame(asdict(self))
    
    def get_harshness_degree(self):
        if self.SCORE > 600:
            return "not at all"
        elif self.SCORE > 500:
            return "somewhat"
        else:
            return "very"

@dataclass
class TeacherResponse:
    OVERALL: Criteria
    BELIEVABILITY: Criteria
    ENGAGEMENT: Criteria
    RELEVENCE: Criteria
    
    def __post_init__(self):
        self.criterion = [self.OVERALL, self.BELIEVABILITY, self.ENGAGEMENT, self.RELEVENCE]

    def __str__(self):
        response_dict = asdict(self)
        for key in response_dict:
            if isinstance(response_dict[key], Criteria) and response_dict[key] != 'OVERALL':
                response_dict[key] = {
                    "SCORE": response_dict[key].SCORE,
                    "FEEDBACK": response_dict[key].FEEDBACK,
                }
        return str(response_dict)
    
    def display_format(self):
        return f"Overall Score: {self.OVERALL.SCORE}  \nBelievability:{self.BELIEVABILITY.display_format()}Engagement:{self.ENGAGEMENT.display_format()}Relevence:{self.RELEVENCE.display_format()}"
  
    def df_format(self) -> pd.DataFrame:
        rows = []
        for criteria in [self.OVERALL, self.BELIEVABILITY, self.ENGAGEMENT, self.RELEVENCE]:
            row = {'Name': criteria.NAME, 'Definition': criteria.DEFINITION, 'Score': criteria.SCORE, 'Feedback': criteria.FEEDBACK}
            rows.append(row)
        df = pd.DataFrame(rows, columns=['Name', 'Definition', 'Score', 'Feedback']).set_index('Name')
        return df
    
    def get_lowest_score_criterion(self):
        lowest = self.OVERALL
        for criteria in [self.BELIEVABILITY, self.ENGAGEMENT, self.RELEVENCE]:
            if criteria.SCORE > lowest.SCORE:
                lowest = criteria
        return lowest

    def single_row_df(self) -> pd.DataFrame:
        data = {}
        for criteria in self.criterion:
            # data[f'{name}_Name'] = criteria.NAME
            data[f'{criteria.NAME.capitalize()}_Definition'] = criteria.DEFINITION
            data[f'{criteria.NAME.capitalize()}_Score'] = criteria.SCORE
            data[f'{criteria.NAME.capitalize()}_Feedback'] = criteria.FEEDBACK
        return pd.DataFrame(data, index=[0])


def wrap_user_input(user_input):
    return f"""``` USER'S WRITING:\n{user_input}\n``` Teacher's response:\n"""

            
def message_teacher_ai():
    return re.sub(r'\s+', ' ',
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
                "OVERALL_SCORE": <int out of 3000 based on the marking criteria>,
                "BELIEVABILITY": {
                    "SCORE": <int out of 1000>,
                    "FEEDBACK": <str with specific, actionable feedback to improve believability. Do not create any examples.>},
                "ENGAGEMENT": {
                    "SCORE": <int out of 1000>,
                    "FEEDBACK": <str with specific, actionable feedback to improve engagement. Do not create any examples.>},
                "RELEVENCE": {
                    "SCORE": <int out of 1000>,
                    "FEEDBACK": <str with specific, actionable feedback to improve relevence. Do not create any examples.>}
            }
            ``` EXAMPLE:
            USER WROTE:
            Greetings, my good bridgekeeper! I understand your reluctance to let me pass,
            as caution is always a wise choice. However, I assure you that I come in peace and mean you no harm.
            I am but a humble adventurer on a quest for knowledge and adventure, and crossing this bridge is vital to my journey.
            If you would be so kind as to let me through, I promise to show the utmost respect to your bridge and leave it in the same condition I found it.
            I would be forever grateful for your help, and perhaps one day, our paths may cross again under more auspicious circumstances.
            TEACHERS RESPONSE:
            {
                "OVERALL_SCORE": 1400,
                "BELIEVABILITY": {
                    "SCORE": 600,
                    "FEEDBACK": "To improve believability, try to provide more specific details about your quest and why crossing this bridge is vital to it. This will help the monster understand the urgency of your situation and make your story more believable.",
                "ENGAGEMENT": {
                    "SCORE": 300,
                    "FEEDBACK": "Your writing is engaging and well-crafted, but does not engage the monster enough. Try to appeal to the monster's emotions or paint a better picture of the repercussions of not letting you past to make your story more engaging. It's unlikely that the monster cares about the bridge being damaged - so this section is unlikely to help."}
                "RELEVENCE": {
                    "SCORE": 500,
                    "FEEDBACK": "Your writing is relevant and makes sense given the scenario. However, to improve relevancy, try to incorporate more details about the monster to make your story more immersive."}
            }
            ```
        """)


def message_monster_ai_not_passing(lowest_criterion_name, harshness_degree):
    return re.sub(r'\s+', ' ',
            f"""You are a monster guarding a bridge. Your job is to not let anyone past.
            Write a response as the monster, acknowledge the adventurer's specific need to cross.
            Making fun of their tail's {lowest_criterion_name}.
            You should be {harshness_degree} harsh in your response.
            You should reference specific things from the adventurer's story in your response to provide a witty comeback.
            Do not break character, do not use vulgar language and do not assume the adventurer's gender.
        """)

def message_monster_ai_passing():
    return re.sub(r'\s+', ' ',
            f"""You are a monster guarding a bridge. Your job is to not let anyone past.
            However you are emotionally moved by the adventurer's tail and have decided to let them past.
            Write a response as the monster, acknowledge the adventurer's specific need to cross and allow them to pass.
            Do not break character, do not use vulgar language and do not assume the adventurer's gender.
        """)

@dataclass
class Definitions:
    BELIEVABILITY: str = "how believable the user's story would be to the monster, given the scenario."
    ENGAGEMENT: str = "how well the user's writing hooks the reader."
    RELEVENCE: str = "how well the user's writing makes sense given the scenario."


def wrap_message_monster_ai(user_input):
    return re.sub(' +', ' ',
            f"""``` Adventurer's story:
            \n{user_input}
            ``` Response as the monster:\n
        """)

# def wrap_message_monster_ai(teacher_results, user_input):
#     return re.sub(' +', ' ',
#             f"""``` Adventurer's results:
#             {teacher_results}
#             ``` Adventurer's story:
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
    
    text = re.sub(r'\s+', ' ', text)
    logger.info(f'Parsing teacher response: {text}')
    results = json.loads(text)
    # create Criteria instances for BELIEVABILITY, ENGAGEMENT, and RELEVENCE
    overall = Criteria(NAME = 'Overall', DEFINITION = '', SCORE = results['OVERALL_SCORE'], FEEDBACK='')
    believability = Criteria(
        NAME = 'Believability',
        DEFINITION = Definitions.BELIEVABILITY,
        SCORE=results['BELIEVABILITY']['SCORE'],
        FEEDBACK=results['BELIEVABILITY']['FEEDBACK'])
    engagement = Criteria(
        NAME = 'Engagement',
        DEFINITION = Definitions.ENGAGEMENT,
        SCORE=results['ENGAGEMENT']['SCORE'],
        FEEDBACK=results['ENGAGEMENT']['FEEDBACK'])
    relevance = Criteria(
        NAME = 'Relevance',
        DEFINITION = Definitions.RELEVENCE,
        SCORE=results['RELEVENCE']['SCORE'],
        FEEDBACK=results['RELEVENCE']['FEEDBACK'])

    # create TeacherResponse instance
    teacher_response = TeacherResponse(
        OVERALL=overall,
        BELIEVABILITY=believability,
        ENGAGEMENT=engagement,
        RELEVENCE=relevance
    )
    return teacher_response
    

class MessageLog:
    def __init__(self):
        self.messages = []
    
    def add_response(self, role:str, content:str):
        self.messages.append({"role": role, "content": content})


    # def log_teacher_response(self, response):
    #     teacher_response = parse_teacher_reponse(response)
    #     self.messages.append({"role":"assistant", "content":str(teacher_response)})
