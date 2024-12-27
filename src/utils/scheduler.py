from time import perf_counter
from typing import List, Dict, Any

from src.representation.flight import Flight
from src.representation.runway import Runway


class ExperimentConfig:
    def __init__(self, algorithm: Any, params: Dict[str, Any]):
        self._algorithm = algorithm
        self._params = params

    def __repr__(self) -> str:
        return f"Algorithm={self._algorithm.__name__}, params={self._params}"

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def params(self):
        return self._params


class Scheduler:
    def __init__(self, experiment: ExperimentConfig):
        self._experiment = experiment

    def evaluate(self, flights: List[Flight], runways: List[Runway]) -> Dict[str, Dict[str, float]]:
        """
        Returns:
            dict: A dictionary where the key is a string combining the algorithm name and parameters,
                  and the value is another dictionary containing:
                  - "cost" (float): The result's cost.
                  - "execution_time" (float): The execution time of the algorithm in seconds.
        """
        results = {}

        start_time = perf_counter()
        algo = self._experiment.algorithm(flights=flights, runways=runways, **self._experiment.params)
        execution_time = perf_counter() - start_time

        result_key = f"{self._experiment.algorithm.__name__}_{self._experiment.params}"
        results[result_key] = {
            "cost": algo.cost,
            "execution_time": execution_time
        }

        return results
