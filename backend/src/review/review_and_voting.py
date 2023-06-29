import logging
from typing import List

from globals import DATABASE
from database.database_calls import add_vote_to_db_log, update_entry_from_vote, get_specific_voted_on_entries
from database.entries import Entry, EntryCombat, calculate_rating_change

logger = logging.getLogger(__name__)


def vote(entries:EntryCombat):
    entries.set_if_wins()
    rating_change = entries.response_a.if_wins
    # update winner's rating
    update_entry_from_vote(DATABASE, entries.response_a.response_id, entries.response_a.elo + rating_change, entries.response_a.vote_count+1)
    
    # update loser's rating
    update_entry_from_vote(DATABASE, entries.response_b.response_id, entries.response_b.elo - rating_change, entries.response_b.vote_count)
    
    add_vote_to_db_log(DATABASE, entries.response_a.response_id, entries.response_b.response_id, rating_change)
    logger.info(f"Vote for {entries.response_a.response_id} cast over {entries.response_b.response_id} for {rating_change} points.")
