import datetime

from src.representation.aircraft import Aircraft
from src.representation.runway import Runway


class Flight:

    def __init__(self, aircraft: Aircraft, flight_id: int, estimated_time_seconds: int, cost_300: float,
                 cost_900: float,
                 cost_1800: float,
                 cost_3600: float) -> None:
        self._aircraft = aircraft
        self.flight_id = flight_id
        self.estimated_time_seconds = estimated_time_seconds
        self._cost_300_seconds = cost_300
        self._cost_900_seconds = cost_900
        self._cost_1800_seconds = cost_1800
        self._cost_3600_seconds = cost_3600
        self.original_estimated_time_seconds = estimated_time_seconds
        self.calculated_time_seconds = estimated_time_seconds
        self.runway: Runway | None = None

    def __repr__(self) -> str:
        return f"Flight(model={self._aircraft.model}, category={self._aircraft.category}, estimated_time={self.seconds_to_timestamp(self.estimated_time_seconds)},  original={self.seconds_to_timestamp(self.original_estimated_time_seconds)}, calculated_time={self.seconds_to_timestamp(self.calculated_time_seconds)}, difference_cost={self.calculated_time_seconds - self.estimated_time_seconds},runway={self.runway})"

    def __lt__(self, other: "Flight") -> bool:
        return self.estimated_time_seconds < other.estimated_time_seconds

    def __eq__(self, other: "Flight") -> bool:
        return self.aircraft == other.aircraft and self.estimated_time_seconds == other.estimated_time_seconds

    @property
    def aircraft(self) -> Aircraft:
        return self._aircraft

    def calculate_landing_time_w_constraints(self, previous_aircraft: "Flight" = None) -> None:
        """
        Calculates the landing time for the current flight while considering the horizontal separation constraints
        from the previous aircraft.
        """
        if previous_aircraft:
            horizontal_separation = self.aircraft.get_horizontal_separation(previous_aircraft.aircraft)
            if self.estimated_time_seconds < previous_aircraft.estimated_time_seconds + horizontal_separation:
                self.estimated_time_seconds = previous_aircraft.estimated_time_seconds + horizontal_separation
            required_landing_time = previous_aircraft.calculated_time_seconds + self.aircraft.get_horizontal_separation(
                previous_aircraft.aircraft)
            self.calculated_time_seconds = max(required_landing_time, self.estimated_time_seconds)
        else:
            self.calculated_time_seconds = self.estimated_time_seconds

    def calculate_estimated_landing_time_w_constraints(self, previous_aircraft: "Flight" = None,
                                                       new_estimated_value: float | int = False) -> float | int:
        """
        Calculates the landing time for the current flight while considering the horizontal separation constraints
        from the previous aircraft.
        """
        if previous_aircraft:
            horizontal_separation = self.aircraft.get_horizontal_separation(previous_aircraft.aircraft)
            required_estimated_landing_time = previous_aircraft.estimated_time_seconds + horizontal_separation
            return max(required_estimated_landing_time, new_estimated_value)
        else:
            return new_estimated_value

    @staticmethod
    def seconds_to_timestamp(time: int) -> str:
        return str(datetime.timedelta(seconds=time))

    def calculate_cost(self, latency_seconds: int) -> float:
        cost: float = 0.0

        intervals = [
            (300, self._cost_300_seconds),
            (900, self._cost_900_seconds),
            (1800, self._cost_1800_seconds),
            (float('inf'), self._cost_3600_seconds),
        ]
        for i, (upper_bound, rate) in enumerate(intervals):
            if latency_seconds > 0:
                if i == 0:
                    lower_bound = 0
                else:
                    lower_bound = intervals[i - 1][0]

                interval_duration = min(upper_bound - lower_bound, latency_seconds)
                cost += interval_duration * rate
                latency_seconds -= interval_duration

        return cost
