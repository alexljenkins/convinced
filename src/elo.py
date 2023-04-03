

def starting_elo():
    return 1200


def calculate_rating_change(current_rating, opponant_rating, score):
    expected_score = 1 / (1 + 10^((opponant_rating - current_rating)/400))
    K = 32
    new_rating = current_rating + K * (score - expected_score)
    
    return int(new_rating)