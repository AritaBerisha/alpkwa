import unittest

from src.representation.aircraft import Aircraft
from src.representation.flight import Flight


class FlightTest(unittest.TestCase):
    flight = None
    previous_flight = None

    def setUp(self):
        aircraft = Aircraft(model="TestModel", category="Test", minimum_required_runway_length=1000)

        self.flight = Flight(
            aircraft=aircraft,
            flight_id=1,
            estimated_time_seconds=0,
            cost_300=2.45,
            cost_900=4.5,
            cost_1800=7.34,
            cost_3600=10.32
        )

        self.previous_flight = Flight(
            aircraft=aircraft,
            flight_id=2,
            estimated_time_seconds=0,
            cost_300=2.45,
            cost_900=4.5,
            cost_1800=7.34,
            cost_3600=10.32
        )

    def tearDown(self):
        self.flight = None
        self.previous_flight = None

    def test_calculate_cost_less_than_300(self):
        cost = self.flight.calculate_cost(latency_seconds=180)
        self.assertEqual(round(cost, 2), 441.00)

    def test_calculate_cost_less_than_900(self):
        cost = self.flight.calculate_cost(latency_seconds=345)
        self.assertEqual(round(cost, 2), 937.50)

    def test_calculate_cost_less_than_1800(self):
        cost = self.flight.calculate_cost(latency_seconds=1000)
        self.assertEqual(round(cost, 2), 4169.00)

    def test_calculate_cost_more_than_1800(self):
        cost = self.flight.calculate_cost(latency_seconds=2050)
        self.assertEqual(round(cost, 2), 12621.00)
