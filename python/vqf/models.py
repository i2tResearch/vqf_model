class Transmitter:

    def __init__(
            self, id: str, name: str, height: float, power: float,
            frequency: float, tilt: float, azimuth: float,
            gain: float, reference: str):
        self.id: str = id
        self.name: str = name
        self.height: float = height
        self.power: float = power
        self.frequency: float = frequency
        self.tilt: float = tilt
        self.azimuth: float = azimuth
        self.gain: float = gain
        self.reference: str = reference
        self.coverage_matrix: list[list[float]] = []

    def __str__(self):
        return f"{self.name}, {self.frequency} (AZ {self.azimuth}, TL {self.tilt}, H: {self.height}, PW: {self.power}, G: {self.gain}, {self.reference})"

    @classmethod
    def from_api_dict(cls, j) -> "Transmitter":
        return Transmitter(
            j["id"], j["name"], j["height"], j["power"],
            j["frequency"], j["tilt"], j["azimuth"],
            j["gain"], j["reference"])


class Site:

    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.transmitters: list[Transmitter] = []

    def __str__(self):
        return f"Lat: {self.latitude}, Lon: {self.longitude}"

    @classmethod
    def from_api_dict(cls, j) -> list["Site"]:
        unique_locations = set(
            [(t["location"]["latitude"], t["location"]["longitude"]) for t in j])
        sites = []
        for l in unique_locations:
            site = Site(l[0], l[1])
            transmitters = filter(
                lambda s: s["location"]["latitude"] == site.latitude and
                s["location"]["longitude"] == site.longitude,
                j)
            site.transmitters = [
                Transmitter.from_api_dict(t) for t in transmitters]
            sites.append(site)
        return sites


class Project:

    def __init__(
            self, id: str, name: str, propagation_model: str,
            avg_receiver_height: float, threshold: float, simulated: bool):
        self.id: str = id
        self.name: str = name
        self.propagation_model: str = propagation_model
        self.avg_receiver_height = avg_receiver_height
        self.threshold: float = threshold
        self.simulated: bool = simulated
        self.sites: list["Site"] = []
        self.coverage_matrix: list[list[float]] = []
        self.distribution_matrix: list[list[int]] = []

    def __str__(self):
        return f"{self.id} {self.name} ({self.propagation_model}, THR {self.threshold}, ARH {self.avg_receiver_height})"

    @classmethod
    def from_api_dict(cls, j) -> "Project":
        return Project(
            j["id"], j["name"], j["propagationModel"],
            j["averageReceiverHeight"], j["threshold"], j["existsSimulation"]
        )

    @classmethod
    def from_api_dict_detailed(cls, j) -> "Project":
        project = cls.from_api_dict(j)
        transmitters = j["transmitterList"]
        project.sites = Site.from_api_dict(transmitters)
        return project

    def number_of_points(self):
        if (len(self.coverage_matrix) > 0):
            return len(self.coverage_matrix) * len(self.coverage_matrix[0])
        else:
            return 0
