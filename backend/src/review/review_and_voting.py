import logging

from src.database.database_calls import add_vote_to_db_log, update_entry_from_vote

logger = logging.getLogger(__name__)


def vote(db, response):
    
    winning_response[5] += rating_change
    update_entry_from_vote(db = db, id = winning_response[0], elo = winning_response[5], vote_count = winning_response[4] + 1)
    
    # loser
    losing_response[5] -= rating_change
    update_entry_from_vote(db = db, id = losing_response[0], elo = losing_response[5], vote_count = losing_response[4] + 1)

    add_vote_to_db_log(db, winning_response, losing_response, rating_change)
