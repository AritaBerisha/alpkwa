import copy
import random
from random import randint
from typing import List

from src.algorithms.first_come_first_served_algorithm import FirstComeFirstServedAlgorithm as Solution
from src.representation.flight import Flight
from src.representation.runway import Runway


class KillerWhaleAlgorithm:
    EARLIEST_TIME = 25200  # 7:00 AM in seconds (in data)
    ITERATIONS = 50
    WEIGHT_DAMPER = 0.99
    MAX_STABLE_ITERATIONS = 10
    POPULATION_SIZE = 100
    NUMBER_OF_LEADERS = 7

    def __init__(self,
                 flights: List[Flight],
                 runways: List[Runway],
                 runway_swap_rate: float,
                 leader_effect: float,
                 global_leader_effect: float,
                 allowed_time_adjustment: int) -> None:
        self.runways = runways
        self.population_size = self.POPULATION_SIZE
        self.iterations = self.ITERATIONS
        self.runway_swap_rate = runway_swap_rate
        self.number_of_leaders = self.NUMBER_OF_LEADERS
        self.weight_damper = self.WEIGHT_DAMPER
        self.leader_effect = leader_effect
        self.global_leader_effect = global_leader_effect
        self.allowed_time_adjustment = allowed_time_adjustment

        self.initial_solution = Solution(copy.deepcopy(flights), runways)
        self.best_solution = self.initial_solution
        self.population: List[Solution] = self._generate_random_population()
        self.run()

        self._validate_solution()
        self.cost: float = self.best_solution.cost

    def _generate_random_population(self) -> List[Solution]:
        random_population = [self.initial_solution]
        for i in range(self.population_size - 1):
            new_random_solution = self._get_random_solution()
            random_population.append(new_random_solution)
        return random_population

    def _get_random_solution(self) -> Solution:
        """Generates a random solution by adjusting flight times and swapping runways based on a certain rate."""
        temp_flights = copy.deepcopy(self.initial_solution.flights)
        first_flight_start_time: int = temp_flights[0].estimated_time_seconds

        for flight in temp_flights:
            if random.random() < self.runway_swap_rate:
                valid_runways = [runway for runway in self.runways if runway.is_valid_runway(flight)]
                flight.runway = random.choice(valid_runways)

        for index, flight in enumerate(temp_flights):
            new_estimated_time: int = flight.estimated_time_seconds + randint(-self.allowed_time_adjustment,
                                                                              self.allowed_time_adjustment)
            flight.estimated_time_seconds = max(new_estimated_time, first_flight_start_time)

        return Solution(temp_flights, self.runways)

    def run(self) -> None:
        leaders = self._get_leaders()
        team_sizes = self._calculate_team_sizes(leaders)

        last_best_cost = float('inf')
        repeated_iterations = 0

        for i in range(self.iterations):
            best_solution_cost = self.best_solution.cost
            if best_solution_cost == last_best_cost:
                repeated_iterations += 1
            else:
                repeated_iterations = 0
            last_best_cost = best_solution_cost
            if repeated_iterations >= self.MAX_STABLE_ITERATIONS:
                break

            self._process_population(leaders, team_sizes)

        self._update_result_w_constraints()

    def _get_leaders(self) -> List[Solution]:
        return sorted(self.population, key=lambda x: x.cost)[:self.number_of_leaders]

    def _calculate_team_sizes(self, leaders: List[Solution]) -> List[float]:
        return ([self.population_size // len(leaders)] * (len(leaders) - 1) +
                [self.population_size - (self.population_size // len(leaders)) * (len(leaders) - 1)])

    def _process_population(self, leaders: List[Solution], team_sizes: List[float]) -> None:
        for team_index, leader in enumerate(leaders):
            team_start = team_index * (self.population_size // len(leaders))
            team_end = team_start + team_sizes[team_index]

            for index, solution in enumerate(self.population[team_start:team_end]):
                self._update_solution(team_start + index, solution, leader)

    def _update_solution(self, index: int, solution: Solution, leader: Solution) -> None:
        temp_solution = self._change_velocity(solution)
        new_solution = self._change_position(temp_solution, self.best_solution, leader)
        self.population[index] = Solution(new_solution.flights, self.runways)

        if self.population[index].cost < self.best_solution.cost:
            self.best_solution = self.population[index]

    def _change_velocity(self, solution: Solution) -> Solution:
        temp_solution = copy.deepcopy(solution)
        for index, flight in enumerate(temp_solution.flights):
            new_estimated_time: float = max(self.weight_damper * flight.estimated_time_seconds,
                                            flight.original_estimated_time_seconds - self.allowed_time_adjustment)
            flight.estimated_time_seconds = max(new_estimated_time, self.EARLIEST_TIME)

        return temp_solution

    def _change_position(self, temp_solution: Solution, global_leader: Solution, leader: Solution) -> Solution:
        for index, flight in enumerate(temp_solution.flights):
            random_value = random.random()
            global_leader_flight_candidate = next(
                global_leader_flight for global_leader_flight in global_leader.flights if
                global_leader_flight.flight_id == flight.flight_id)
            leader_flight_candidate = next(
                leader_flight for leader_flight in leader.flights if leader_flight.flight_id == flight.flight_id)

            if random_value < self.global_leader_effect:
                flight.runway = global_leader_flight_candidate.runway
            elif random_value < self.global_leader_effect + self.leader_effect:
                flight.runway = leader_flight_candidate.runway

        return temp_solution

    def _update_result_w_constraints(self) -> None:
        for index, flight in enumerate(self.best_solution.flights):
            previous_flight: Flight = self.best_solution.flights[index - 1]
            if flight.runway == previous_flight.runway:
                flight.calculate_landing_time_w_constraints(self.best_solution.flights[index - 1])

    def _validate_solution(self) -> None:
        for index, flight in enumerate(self.best_solution.flights):
            if index == 0:
                continue
            previous_flight = self.best_solution.flights[index - 1]
            if flight.runway.name != previous_flight.runway.name:
                continue
            horizontal_separation = flight.aircraft.get_horizontal_separation(previous_flight.aircraft)
            if flight.calculated_time_seconds < previous_flight.calculated_time_seconds + horizontal_separation:
                print(f"Separation violation detected between {flight} and {previous_flight}")
