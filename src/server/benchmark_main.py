import pstats
from pstats import SortKey
import cProfile
import random
from src.cvrp.ga import GA
from .utils import utils
from .main import build_first_gen
from tqdm import tqdm

BENCHMARK = "M-n110-k10-s9.evrp"

SIZE = 16
IT = 16

random.seed(8)
INSTANCE = utils.create_ecvrp(utils.parse_dataset(BENCHMARK))

ga_runner = GA(
    build_first_gen(SIZE, INSTANCE),
    0.2,
    8
).run(IT)


def runner():
    for _ in tqdm(ga_runner, total=IT):
        pass


cProfile.run("runner()", "benchmark")

p = pstats.Stats("benchmark")
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(30)

