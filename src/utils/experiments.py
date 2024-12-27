from src.algorithms.contrained_position_shifting_algorithm import ConstrainedPositionShifting
from src.algorithms.first_come_first_served_algorithm import FirstComeFirstServedAlgorithm
from src.algorithms.killer_whale_algorithm import KillerWhaleAlgorithm
from src.utils.scheduler import ExperimentConfig

first_come_first_served_experiments = [
    ExperimentConfig(FirstComeFirstServedAlgorithm, {})
]

constrained_position_shifting_experiments = [
    ExperimentConfig(ConstrainedPositionShifting, {"max_shifts": max_shifts})
    for max_shifts in range(1, 5)
]

killer_whale_experiments = [
    ExperimentConfig(KillerWhaleAlgorithm, {
        "runway_swap_rate": runway_swap_rate,
        "leader_effect": leader_effect,
        "global_leader_effect": global_leader_effect,
        "allowed_time_adjustment": allowed_time_adjustment
    })
    for
    runway_swap_rate, leader_effect, global_leader_effect, allowed_time_adjustment
    in [
        # Experimental
        # (0.8, 0.8, 0.2, 20, 2),
        # (0.8, 0.8, 0.2, 20, 3),
        # (0.8, 0.8, 0.2, 20, 4),
        # (0.2, 0.2, 0.8, 60, 2),
        # (0.2, 0.2, 0.8, 60, 3),
        # (0.2, 0.2, 0.8, 60, 4),
        # (0.8, 0.8, 0.2, 20, 2),
        # (0.8, 0.8, 0.2, 40, 2),
        # (0.8, 0.8, 0.2, 60, 2),
        # (0.2, 0.2, 0.8, 20, 4),
        # (0.2, 0.2, 0.8, 40, 4),
        # (0.2, 0.2, 0.8, 60, 4),
        # (0.8, 0.8, 0.2, 20, 2),
        # (0.8, 0.6, 0.4, 20, 2),
        # (0.8, 0.4, 0.6, 20, 2),
        # (0.8, 0.2, 0.8, 20, 2),
        # (0.2, 0.8, 0.2, 60, 4),
        # (0.2, 0.6, 0.4, 60, 4),
        # (0.2, 0.4, 0.6, 60, 4),
        # (0.2, 0.2, 0.8, 60, 4),
        # (0.2, 0.8, 0.2, 20, 2),
        # (0.4, 0.8, 0.2, 20, 2),
        # (0.6, 0.8, 0.2, 20, 2),
        # (0.8, 0.8, 0.2, 20, 2),
        # (0.2, 0.2, 0.8, 60, 4),
        # (0.4, 0.2, 0.8, 60, 4),
        (0.6, 0.2, 0.8, 60),
        (0.8, 0.2, 0.8, 60),
        (0.8, 0.8, 0.2, 20),
    ]
]

experiments = first_come_first_served_experiments + constrained_position_shifting_experiments + killer_whale_experiments
