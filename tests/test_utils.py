from app.utils import calculate_distance

def test_calculate_distance():
    coord1 = (10.0, 20.0)
    coord2 = (10.1, 20.1)
    distance = calculate_distance(coord1, coord2)
    assert round(distance, 2) == 15.57
