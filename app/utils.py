import logging
from geopy.distance import geodesic
from geopy.exc import GeopyError

logger = logging.getLogger(__name__)

def calculate_distance(coord1, coord2):
    try:
        logger.debug(f"Calculating distance between {coord1} and {coord2}")
        distance = geodesic(coord1, coord2).km
        logger.info(f"Distance calculated: {distance} km")
        return distance
    except GeopyError as e:
        logger.error("Error calculating distance with geopy: %s", str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        raise
