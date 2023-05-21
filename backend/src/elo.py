import logging

logger = logging.getLogger(__name__)

def starting_elo():
    return 1200


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