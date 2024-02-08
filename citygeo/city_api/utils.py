import math


class GeoUtils:
    @staticmethod
    def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the distance between two points on the Earth
        """
        R = 6371  # Radius of the Earth in kilometers
        d_lat = GeoUtils.deg2rad(lat2 - lat1)  # Difference in latitude in radians
        d_lon = GeoUtils.deg2rad(lon2 - lon1)  # Difference in longitude in radians
        a = (
                math.sin(d_lat / 2) * math.sin(d_lat / 2) +
                math.cos(GeoUtils.deg2rad(lat1)) * math.cos(GeoUtils.deg2rad(lat2)) *
                math.sin(d_lon / 2) * math.sin(d_lon / 2)
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c  # Distance in kilometers
        return d

    @staticmethod
    def deg2rad(deg: float) -> float:
        """
        Convert degrees to radians.
        """
        return deg * (math.pi / 180)
