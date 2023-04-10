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

    def __init__(self, id: int, name: str, avg_receiver_height: float, propagation_model: str, threshold: float, simulated: bool):
        self.id: int = id
        self.name: str = name
        self.avg_receiver_height = avg_receiver_height
        self.propagation_model: str = propagation_model
        self.threshold: float = threshold
        self.simulated: bool = simulated

    def __str__(self):
        return f"{self.id} {self.name} ({self.propagation_model}, THR {self.threshold}, ARH {self.avg_receiver_height})"

    @classmethod
    def from_api_dict(cls, j) -> "Project":
        return Project(j["id"], j["name"], j["averageReceiverHeight"], j["propagationModel"], j["threshold"], j["existsSimulation"])
