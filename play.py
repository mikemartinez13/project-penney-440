from penney_db1 import make_database
from visualization import heatmap
from simulation import sim

def play(path, ngames: int, seed = 0) -> None:
    simulation = sim(ngames, seed)
    db_path = make_database(simulation, path)

    return 