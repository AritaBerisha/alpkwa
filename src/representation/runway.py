class Runway:

    def __init__(self, name: str, length: int) -> None:
        self.name = name
        self.length = length

    def __repr__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other_runway: "Runway") -> bool:
        return self.name == other_runway.name

    def is_valid_runway(self, flight) -> bool:
        return self.length > flight.aircraft.minimum_required_runway_length