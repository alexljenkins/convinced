from pydantic import BaseModel
from typing import Any, Optional
from pydantic.dataclasses import dataclass


class Entry(BaseModel):
    response_id: Optional[int] = None
    user_input: Optional[str] = ''
    character_response: Optional[str] = ''
    vote_count: int = 0
    elo: int = 1200
    enabled: bool = True
    if_wins:int = 0

    @classmethod
    def from_list(cls, values):
        return cls(response_id = values[0], user_input = values[1], character_response = values[2], vote_count = values[3], elo = values[4], enabled = values[5])
    
    def to_dict(self):
        return {
            "response_id": self.response_id,
            "user_input": self.user_input,
            # "character_response": self.character_response,
            "vote_count": self.vote_count,
            "elo": self.elo,
            # "enabled": self.enabled
        }

    def to_db(self):
        return [self.user_input, self.character_response, self.vote_count, self.elo, self.enabled]


class EntryCombat(BaseModel):
    response_a: Entry
    response_b: Entry

    def set_if_wins(self):
        self.response_a.if_wins = calculate_rating_change(self.response_a.elo, self.response_b.elo, outcome=1)
        self.response_b.if_wins = calculate_rating_change(self.response_b.elo, self.response_a.elo, outcome=1)

    def get_voting_data(self):
        response_a = self.response_a.to_dict()
        response_a['if_wins'] = calculate_rating_change(self.response_a.elo, self.response_b.elo, outcome=1)
        response_b = self.response_b.to_dict()
        response_b['if_wins'] = calculate_rating_change(self.response_b.elo, self.response_a.elo, outcome=1)
        return [response_a, response_b]



def calculate_rating_change(current_rating, opponant_rating, outcome=1):
    """

    Args:
        current_rating (int): rating of the text before this vote
        opponant_rating (int): rating of the opponent's text before this vote
        outcome (int): 1 = voted for, 0 = voted against the text

    Returns:
        new rating for that response (changed by a max of 32 points in either direction)
    """
    expected_score = 1 / (1 + 10**((opponant_rating - current_rating)/400))
    K = 32
    rating_change = int(abs(K * (outcome - expected_score)))
    # logger.info(f"Results: {current_rating} beat {opponant_rating}, Rating change: {rating_change}")
    return rating_change