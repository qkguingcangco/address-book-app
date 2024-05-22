from geopy.distance import geodesic

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km # returns calculated distance in kilometers
