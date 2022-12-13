from .ecvrp import ECVRPInstance, ECVRPSolution
from . import constraints_validators
import random
from .ga import GA
from src.server.utils import utils
from tqdm import tqdm


def build_first_gen(size: int, instance: ECVRPInstance):
    """Does stuff"""
    validators = [
        constraints_validators.BatteryTWValidator(),
        constraints_validators.CapacityValidator(),
        constraints_validators.VehiculeCountValidator()
    ]

    towns = instance.get_towns()

    first_gen = []
    counter = 0

    t = tqdm(total=size)

    while len(first_gen) < size:
        counter += 1
        solution = [*towns]
        random.shuffle(solution)

        cum_dem = 0
        insert_points = []

        for i, p in enumerate(solution):
            cum_dem += bench.get_demand(p)
            if cum_dem > bench.get_ev_capacity():
                insert_points.append(i-1 + len(insert_points))
                cum_dem = 0

        if len(insert_points) > bench.get_ev_count():
            continue

        for p in insert_points:
            solution.insert(p, bench.get_depot())

        solution.insert(0, instance.get_depot())
        solution.append(instance.get_depot())
        element = ECVRPSolution(validators, solution, instance)

        # When mutating the solution kind of auto correct itself.
        # If we don't apply this auto correction there is no way
        # we produce a single valid solution.
        element.validate()

        if element.is_valid():
            first_gen.append(element)
            t.update()
    t.close()
    return first_gen


if __name__ == "__main__":
    bench = utils.create_ecvrp(utils.parse_dataset("E-n60-k5-s9.evrp"))
    # build_first_gen(8, bench)

    g_a = GA(build_first_gen(8, bench), 0.1)

    for g in tqdm(g_a.run(60)):
        pass
