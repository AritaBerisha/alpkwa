from typing import List

from src.representation.flight import Flight


class Performance:

    @staticmethod
    def get_cost(flights: List[Flight]) -> float:
        total_cost_euros: float = 0.0
        for flight in flights:
            latency_seconds: int = max(0, flight.calculated_time_seconds - flight.original_estimated_time_seconds)
            total_cost_euros += flight.calculate_cost(latency_seconds)

        return round(total_cost_euros, 2)
