import pytest

from api.elo import calculate_rating_change


@pytest.mark.parametrize("current_rating, opponant_rating, outcome, expected_new_rating",
                    [
                        (1200, 1200, 1, 16),
                        (1200, 1200, 0, 16),
                        (1500, 1200, 1, 4),
                        (1200, 1500, 0, 4),
                        (1500, 1200, 0, 27),
                        (1200, 1500, 1, 27),
                        (2200, 1500, 1, 0),
                        (1500, 2200, 0, 0),
                        (2200, 1500, 0, 31),
                        (1500, 2200, 1, 31),
                    ],
                )
def test_calculate_rating_change(current_rating, opponant_rating, outcome, expected_new_rating):
    assert calculate_rating_change(current_rating, opponant_rating, outcome) == expected_new_rating