from abc import ABC, abstractmethod


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

    # --- WP-202: Operator Overloading ---
    def __add__(self, other: "Distance") -> "Distance":
        if self.unit == other.unit:
            return Distance(self.magnitude + other.magnitude, self.unit)
        other_converted = other.convert()
        return Distance(self.magnitude + other_converted.magnitude, self.unit)

    def __sub__(self, other: "Distance") -> "Distance":
        other_val = other.magnitude if self.unit == other.unit else other.convert().magnitude
        diff = self.magnitude - other_val
        if diff < 0:
            raise ValueError("Distance result cannot be negative.")
        return Distance(diff, self.unit)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Distance):
            return False
        other_val = other.magnitude if self.unit == other.unit else other.convert().magnitude
        return abs(self.magnitude - other_val) < 0.001

    def __lt__(self, other: "Distance") -> bool:
        other_val = other.magnitude if self.unit == other.unit else other.convert().magnitude
        return self.magnitude < other_val

    def __gt__(self, other: "Distance") -> bool:
        other_val = other.magnitude if self.unit == other.unit else other.convert().magnitude
        return self.magnitude > other_val

    def __repr__(self) -> str:
        return f"Distance({self.magnitude:.2f}, '{self.unit}')"

    def __str__(self) -> str:
        return f"{self.magnitude:.2f} {self.unit}"


# --- WP-205: Mixins ---
class ElevationMixin:
    def grade_percentage(self) -> float:
        dist_m = self.distance.magnitude * 1000 if self.distance.unit == "km" else self.distance.magnitude * 1609.34
        return (self.elevation_gain_m / dist_m) * 100 if dist_m > 0 else 0.0


class RatingMixin:
    def average_stars(self) -> float:
        return 4.5


# --- WP-201: Abstract Base Class ---
class Trail(ABC):
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

    @abstractmethod
    def estimated_time(self) -> float:
        """Returns estimated time in hours."""
        pass

    @abstractmethod
    def summary(self) -> str:
        pass

    def __eq__(self, other):
        if isinstance(other, Trail):
            return self.id == other.id
        return False


# --- WP-201 & WP-203: Concrete Subclasses ---
class DayHike(Trail, ElevationMixin):
    def estimated_time(self) -> float:
        return self.distance.magnitude / 4.0

    def summary(self) -> str:
        return f"Day Hike: {self.name} ({self.distance})"


class BackpackingRoute(Trail):
    def estimated_time(self) -> float:
        return (self.distance.magnitude / 3.0) + (self.elevation_gain_m / 400.0)

    def summary(self) -> str:
        return f"Backpacking: {self.name} ({self.distance})"


class GuidedDayHike(DayHike, RatingMixin):
    def __init__(self, trail_id: str, name: str, distance: Distance, elevation_gain_m: int, difficulty: str, guide_name: str):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.guide_name = guide_name


# --- WP-206: Duck-typed Fake Trail ---
class DuckTypeFakeTrail:
    def __init__(self, name: str):
        self.name = name

    def estimated_time(self) -> float:
        return 1.5

    def summary(self) -> str:
        return f"Fake Trail: {self.name}"


class Itinerary:
    def __init__(self, name: str):
        self.name = name
        self.trails = []

    def add_trail(self, trail):
        self.trails.append(trail)

    def total_distance(self) -> float:
        return sum(t.distance.magnitude for t in self.trails)