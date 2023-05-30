import logging
from typing import List

from src.globals import DATABASE
from src.database.database_calls import add_vote_to_db_log, update_entry_from_vote
from src.database.entries import Entry, EntryCombat

logger = logging.getLogger(__name__)



def parse_vote_api_data(api_vote_data) -> List[Entry]:
    
    entries = []
    for item in api_vote_data:
        entry = Entry(
            response_id=int(item.get('response_id')),
            user_input=item.get('user_input'),
            vote_count=int(item.get('vote_count')),
            elo=int(item.get('elo')),
        )
        entry['if_wins'] = int(item.get('if_wins'))
        entries.append(entry)
    
    return entries


def vote(entries:List[Entry], winner_id:int):
    for entry in entries:
        if entry.response_id == winner_id:
            update_entry_from_vote(DATABASE, entry.response_id, entry.elo + entry.if_wins, entry.vote_count+1)
            rating_change = entry.if_wins
        else:  # update as loser
            update_entry_from_vote(DATABASE, entry.response_id, entry.elo - entry.if_wins, entry.vote_count)
            loser_id = entry.response_id
    
    add_vote_to_db_log(DATABASE, winner_id, loser_id, rating_change)
