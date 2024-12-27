import os
from typing import List

import pandas as pd

from src.representation.aircraft import Aircraft
from src.representation.flight import Flight
from src.representation.runway import Runway


class FlightManager:
    def __init__(self, filepath: str):
        self._filepath = filepath

    def _read_csv(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self._filepath, filename), header=0)

    def _get_aircraft_details(self, filename: str) -> dict[str, dict[str, int]]:
        aircraft_data = self._read_csv(filename)
        return {
            row['model']: {
                "runway_length": row['minimum_required_runway_length'],
                "buffer_time": row['buffer_time'],
            }
            for _, row in aircraft_data.iterrows()
        }

    def load_flights(self, filename: str, aircraft_filename: str) -> List[Flight]:
        flight_data = self._read_csv(filename)
        aircraft_data = self._get_aircraft_details(aircraft_filename)

        flights = [
            Flight(
                aircraft=Aircraft(
                    model=row['mdl'],
                    category=row['category'],
                    minimum_required_runway_length=aircraft_data.get(row['mdl'])["runway_length"],
                    buffer_time=aircraft_data.get(row["mdl"])["buffer_time"],
                ),
                flight_id=row['id'],
                estimated_time_seconds=row['sta_s'],
                cost_300=row['cost_300'],
                cost_900=row['cost_900'],
                cost_1800=row['cost_1800'],
                cost_3600=row['cost_3600']
            )
            for _, row in flight_data.iterrows()
        ]

        return flights

    def load_runways(self, filename: str) -> List[Runway]:
        """Loads runway data and returns a list of Runway objects."""
        runway_data = self._read_csv(filename)
        return [
            Runway(name=row['name'], length=row['length'])
            for _, row in runway_data.iterrows()
        ]
