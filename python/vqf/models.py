class Antenna:

    def __init__(self, azimuth: float, tilt: float, power: float):
        self.azimuth: float = azimuth
        self.tilt: float = tilt
        self.power: float = power


class Site:

    def __init__(self, id: str, latitude: str, longitude: str, user_id: str):
        self.id: str = id
        self.latitude: str = latitude
        self.longitude: str = longitude
        self.user_id: str = user_id
        self.antennas: list[Antenna] = []


class Project:

    def __init__(self, sites: list[Site]):
        self.sites: list[Site] = sites
