from typing import List, Dict

from src.utils.performance import Performance
from src.representation.flight import Flight
from src.representation.runway import Runway


class FirstComeFirstServedAlgorithm:

    def __init__(self, flights: List[Flight], runways: List[Runway]) -> None:
        self.flights: List[Flight] = flights
        self.runways: List[Runway] = runways

        self.run()
        self.cost: float = Performance.get_cost(self.flights)

    def __eq__(self, other: "FirstComeFirstServedAlgorithm") -> bool:
        return all(f1 == f2 for f1, f2 in zip(self.flights, other.flights))

    def run(self) -> None:
        runway_groups: Dict[str, List[Flight]] = {}

        for index, flight in enumerate(self.flights):
            if flight.runway is None:
                valid_runways = [runway for runway in self.runways if runway.is_valid_runway(flight)]
                flight.runway = valid_runways[index % len(valid_runways)]
            runway_groups.setdefault(flight.runway.name, []).append(flight)

        for runway, flights in runway_groups.items():
            flights.sort(key=lambda f: f.estimated_time_seconds)

        for runway in runway_groups.values():
            previous_aircraft: Flight | None = None
            for flight in runway:
                flight.calculate_landing_time_w_constraints(previous_aircraft)
                previous_aircraft = flight
