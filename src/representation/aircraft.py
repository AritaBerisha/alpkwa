from typing import Dict, Tuple


class Aircraft:
    HEAVY_HEAVY_HORIZONTAL_SEPARATION: int = 96
    HEAVY_MEDIUM_HORIZONTAL_SEPARATION: int = 157
    HEAVY_LIGHT_HORIZONTAL_SEPARATION: int = 196
    MEDIUM_HEAVY_HORIZONTAL_SEPARATION: int = 60
    MEDIUM_MEDIUM_HORIZONTAL_SEPARATION: int = 69
    MEDIUM_LIGHT_HORIZONTAL_SEPARATION: int = 131
    LIGHT_HEAVY_HORIZONTAL_SEPARATION: int = 60
    LIGHT_MEDIUM_HORIZONTAL_SEPARATION: int = 69
    LIGHT_LIGHT_HORIZONTAL_SEPARATION: int = 82

    LIGHT_AIRCRAFT_RUNWAY_TO_TAXI_BUFFER_TIME_SECONDS: int = 15
    MEDIUM_AIRCRAFT_RUNWAY_TO_TAXI_BUFFER_TIME_SECONDS: int = 60
    HEAVY_AIRCRAFT_RUNWAY_TO_TAXI_BUFFER_TIME_SECONDS: int = 90

    horizontal_separation_lookup: Dict[Tuple[str, str], int] = {
        ('Heavy', 'Heavy'): HEAVY_HEAVY_HORIZONTAL_SEPARATION,
        ('Heavy', 'Medium'): HEAVY_MEDIUM_HORIZONTAL_SEPARATION,
        ('Heavy', 'Light'): HEAVY_LIGHT_HORIZONTAL_SEPARATION,
        ('Medium', 'Heavy'): MEDIUM_HEAVY_HORIZONTAL_SEPARATION,
        ('Medium', 'Medium'): MEDIUM_MEDIUM_HORIZONTAL_SEPARATION,
        ('Medium', 'Light'): MEDIUM_LIGHT_HORIZONTAL_SEPARATION,
        ('Light', 'Heavy'): LIGHT_HEAVY_HORIZONTAL_SEPARATION,
        ('Light', 'Medium'): LIGHT_MEDIUM_HORIZONTAL_SEPARATION,
        ('Light', 'Light'): LIGHT_LIGHT_HORIZONTAL_SEPARATION
    }

    def __init__(self, model: str, category: str, minimum_required_runway_length: int, buffer_time) -> None:
        self.model = model
        self.category = category
        self.minimum_required_runway_length = minimum_required_runway_length
        self.buffer_time = buffer_time

    def __repr__(self) -> str:
        return f"Aircraft({self.model}, {self.category})"

    def get_horizontal_separation(self, previous_aircraft: "Aircraft") -> int:
        return self.horizontal_separation_lookup[previous_aircraft.category, self.category] + self.buffer_time
