class Antenna:

    def __init__(self, id: str, name: str, azimuth: float, tilt: float, power: float):
        self.id: str = id
        self.name: str = name
        self.azimuth: float = azimuth
        self.tilt: float = tilt
        self.power: float = power

    def __str__(self):
        return f"{self.name} (AZ {self.azimuth}, TL {self.tilt}, PW: {self.power})"

    @classmethod
    def from_api_dict(cls, j) -> "Antenna":
        return Antenna(j["id"], j["name"], j["azimuth"], j["tilt"], j["power"])


class Site:

    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.antennas: list[Antenna] = []

    def __str__(self):
        return f"Lat: {self.latitude}, Lon: {self.longitude}"

    @classmethod
    def from_api_dict(cls, j) -> list["Site"]:
        unique_locations = set(
            [(t["location"]["latitude"], t["location"]["longitude"]) for t in j])
        sites = []
        for l in unique_locations:
            site = Site(l[0], l[1])
            antennas = filter(
                lambda s: s["location"]["latitude"] == site.latitude and
                s["location"]["longitude"] == site.longitude,
                j)
            site.antennas = [Antenna.from_api_dict(a) for a in antennas]
            sites.append(site)
        return sites


class Project:

    def __init__(
            self, id: int, name: str, avg_receiver_height: float,
            propagation_model: str, threshold: float, simulated: bool):
        self.id: int = id
        self.name: str = name
        self.avg_receiver_height = avg_receiver_height
        self.propagation_model: str = propagation_model
        self.threshold: float = threshold
        self.simulated: bool = simulated
        self.sites: list["Site"] = []

    def __str__(self):
        return f"{self.id} {self.name} ({self.propagation_model}, THR {self.threshold}, ARH {self.avg_receiver_height})"

    @classmethod
    def from_api_dict(cls, j) -> "Project":
        return Project(
            j["id"], j["name"], j["averageReceiverHeight"],
            j["propagationModel"], j["threshold"], j["existsSimulation"]
        )

    @classmethod
    def from_api_dict_detailed(cls, j) -> "Project":
        project = cls.from_api_dict(j)
        transmitters = j["transmitterList"]
        project.sites = Site.from_api_dict(transmitters)
        return project


class OptimizationProperties:

    def __init__(self, signal_levels: list[list[float]]):
        self.signal_levels: list[list[float]] = signal_levels

    def count_points_without_coverage(self, threshold: float) -> int:
        count = 0
        for i in self.signal_levels:
            for j in i:
                if j <= threshold:
                    count += 1
        return count
