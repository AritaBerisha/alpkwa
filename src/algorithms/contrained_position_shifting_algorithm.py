from typing import List, Dict
import copy

from .first_come_first_served_algorithm import FirstComeFirstServedAlgorithm as Solution
from src.utils.performance import Performance
from src.representation.flight import Flight
from src.representation.runway import Runway


class ConstrainedPositionShifting:

    def __init__(self, flights: List[Flight], runways: List[Runway], max_shifts: int = 0) -> None:
        self.flights = flights
        self.runways = runways
        self.max_shifts = max_shifts

        self.initial_solution = Solution(copy.deepcopy(flights), runways)
        self.run()

        self.cost: float = Performance.get_cost(self.flights)

    def run(self) -> None:
        runway_groups: Dict[str, List[Flight]] = {}

        for flight in self.initial_solution.flights:
            runway_groups.setdefault(flight.runway.name, []).append(flight)

        for flights in runway_groups.values():
            flights.sort(key=lambda f: f.estimated_time_seconds)

        for runway, flights in runway_groups.items():
            self._apply_shifts(flights)

    def _apply_shifts(self, runway_flights: List[Flight]) -> None:
        for index in range(len(runway_flights)):
            self._shift_flights(index, runway_flights)

    def _shift_flights(self, index, runway_flights: List[Flight]) -> None:
        current_solution = Solution(self.flights, self.runways)

        for next_shift_index in range(index + 1, min(index + self.max_shifts + 1, len(runway_flights))):
            temp_flights = copy.deepcopy(self.flights)

            temp_flights[index].estimated_time_seconds, temp_flights[next_shift_index].estimated_time_seconds = \
                temp_flights[next_shift_index].estimated_time_seconds, temp_flights[
                    index].estimated_time_seconds

            temp_flights = sorted(temp_flights, key=lambda f: f.estimated_time_seconds)
            temp_solution = Solution(temp_flights, self.runways)

            if temp_solution.cost < current_solution.cost:
                self.flights = temp_flights
