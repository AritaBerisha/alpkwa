import unittest

from src.representation.aircraft import Aircraft


class AircraftTest(unittest.TestCase):
    aircraft = None
    previous_aircraft = None

    def setUp(self):
        self.aircraft = Aircraft(model="TestModel", category="Test", minimum_required_runway_length=1000)
        self.previous_aircraft = Aircraft(model="TestModel", category="Test", minimum_required_runway_length=1000)

    def tearDown(self):
        self.aircraft = None
        self.previous_aircraft = None

    def test_get_horizontal_separation_heavy_after_heavy(self):
        self.aircraft.category = "Heavy"
        self.previous_aircraft.category = "Heavy"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 96)

    def test_get_horizontal_separation_medium_after_heavy(self):
        self.aircraft.category = "Medium"
        self.previous_aircraft.category = "Heavy"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 157)

    def test_get_horizontal_separation_light_after_heavy(self):
        self.aircraft.category = "Light"
        self.previous_aircraft.category = "Heavy"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 196)

    def test_get_horizontal_separation_heavy_after_medium(self):
        self.aircraft.category = "Heavy"
        self.previous_aircraft.category = "Medium"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 60)

    def test_get_horizontal_separation_medium_after_medium(self):
        self.aircraft.category = "Medium"
        self.previous_aircraft.category = "Medium"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 69)

    def test_get_horizontal_separation_light_after_medium(self):
        self.aircraft.category = "Light"
        self.previous_aircraft.category = "Medium"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 131)

    def test_get_horizontal_separation_heavy_after_light(self):
        self.aircraft.category = "Heavy"
        self.previous_aircraft.category = "Light"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 60)

    def test_get_horizontal_separation_medium_after_light(self):
        self.aircraft.category = "Medium"
        self.previous_aircraft.category = "Light"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 69)

    def test_get_horizontal_separation_light_after_light(self):
        self.aircraft.category = "Light"
        self.previous_aircraft.category = "Light"
        self.assertEqual(self.aircraft.get_horizontal_separation(self.previous_aircraft), 82)
