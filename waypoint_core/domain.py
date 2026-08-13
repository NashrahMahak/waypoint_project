# waypoint_core/domain.py

class Distance:
    def __init__(self, magnitude: float, unit: str = "km"):
        if magnitude < 0:
            raise ValueError("Magnitude cannot be negative.")
        if unit not in ["km", "mi"]:
            raise ValueError("Unit must be 'km' or 'mi'.")
        self._magnitude = float(magnitude)
        self._unit = unit

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def unit(self) -> str:
        return self._unit

    def convert(self) -> "Distance":
        if self._unit == "km":
            return Distance(self._magnitude * 0.621371, "mi")
        else:
            return Distance(self._magnitude * 1.60934, "km")

    def __repr__(self):
        return f"{self._magnitude:.2f} {self._unit}"


class Trail:
    default_unit = "km"
    ALLOWED_DIFFICULTIES = {"easy", "moderate", "hard", "expert"}

    def __init__(self, trail_id: str, name: str, distance: Distance, elevation_gain_m: int, difficulty: str):
        self.id = trail_id
        self.name = name
        self.distance = distance
        self.elevation_gain_m = elevation_gain_m
        self._difficulty = None
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty: str):
        if difficulty.lower() not in self.ALLOWED_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty. Allowed: {self.ALLOWED_DIFFICULTIES}")
        self._difficulty = difficulty.lower()

    @classmethod
    def set_default_unit(cls, unit: str):
        if unit in ["km", "mi"]:
            cls.default_unit = unit

    @classmethod
    def from_dict(cls, data: dict) -> "Trail":
        dist = Distance(data["distance_val"], data.get("unit", cls.default_unit))
        return cls(data["id"], data["name"], dist, data["elevation"], data["difficulty"])

    def __eq__(self, other):
        if isinstance(other, Trail):
            return self.id == other.id
        return False


class Itinerary:
    def __init__(self, name: str):
        self.name = name
        self.trails = []

    def add_trail(self, trail: Trail):
        self.trails.append(trail)

    def total_distance(self) -> float:
        return sum(t.distance.magnitude for t in self.trails)