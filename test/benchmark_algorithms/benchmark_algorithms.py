import unittest
from typing import List

from src.algorithms.first_come_first_served_algorithm import FirstComeFirstServedAlgorithm
from src.algorithms.contrained_position_shifting_algorithm import ConstrainedPositionShifting
from src.utils.flight_manager import FlightManager
from src.representation.flight import Flight
from src.representation.runway import Runway


class BenchmarkAlgorithms(unittest.TestCase):
    flights = None
    runways = None

    def setUp(self):
        flight_file = "flights/data_7_11.csv"
        runway_file = "airports/ORY_runways.csv"
        aircraft_file = "aircraft/details.csv"
        manager = FlightManager("../../data")
        self.flights: List[Flight] = manager.load_flights(flight_file, aircraft_file)
        self.runways: List[Runway] = manager.load_runways(runway_file)

    def test_first_come_first_served_algorithm(self):
        algorithm = FirstComeFirstServedAlgorithm(self.flights, self.runways)
        self.assertEqual(algorithm.cost, 2065.25)

    def test_constrained_position_shifting_max_shift_3(self):
        algorithm = ConstrainedPositionShifting(flights=self.flights, runways=self.runways, max_shifts=3)
        self.assertEqual(algorithm.cost, 1902.14)
