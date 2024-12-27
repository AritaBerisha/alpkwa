import argparse
from concurrent.futures import ThreadPoolExecutor
from typing import List

from src.utils.flight_manager import FlightManager
from src.utils.experiments import experiments
from src.utils.scheduler import Scheduler, ExperimentConfig
from src.representation.flight import Flight
from src.representation.runway import Runway


def evaluate_dataset(filepath: str, files: dict[str, str], experiment: ExperimentConfig) -> dict[str, dict[str, float]]:
    """Evaluates the dataset based on the provided experiment configuration and dataset files."""
    manager = FlightManager(filepath)
    flights: List[Flight] = manager.load_flights(files["flights"], files["aircraft"])
    runways: List[Runway] = manager.load_runways(files["runways"])

    scheduler = Scheduler(experiment)
    return scheduler.evaluate(flights, runways)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run experiments on flight scheduling.")
    parser.add_argument("--airport", dest="airport", default="ORY", help="Airport code (default: 'ORY')")
    parser.add_argument("--aircraft_file", dest="aircraft_file", default="details.csv",
                        help="Choose if you want to take into account runway->taxi buffer time.")
    parser.add_argument("--data_file", dest="data_file", default="data_7_11.csv",
                        help="CSV data file (default: 'data_7_11.csv')")

    return parser.parse_args()


def prepare_files(airport: str, aircraft_file: str, data_file: str) -> dict[str, str]:
    return {
        "flights": f"flights/{data_file}",
        "runways": f"airports/{airport}_runways.csv",
        "aircraft": f"aircraft/{aircraft_file}",
    }


def print_results(results: dict[str, dict[str, float]]) -> None:
    for algorithm, result in results.items():
        print(f"Algorithm: {algorithm} | Cost: {result['cost']} | Execution Time: {result['execution_time']} seconds")


def run_experiments(experiment_configs: List[ExperimentConfig], filepath: str, files: dict[str, str]) -> None:
    """Runs the Experiment Configurations on Parallel."""
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(evaluate_dataset, filepath, files, experiment): experiment
            for experiment in experiment_configs
        }

        for future in futures:
            results = future.result()
            print_results(results)


def main() -> None:
    args = parse_arguments()

    filepath = "data/"
    files = prepare_files(args.airport, args.aircraft_file, args.data_file)

    run_experiments(experiments, filepath, files)


if __name__ == '__main__':
    main()
