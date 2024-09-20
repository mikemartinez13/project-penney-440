from data_mgmt.penney_db1 import make_database
from visuals.visualization import heatmap
from sim.simulation import sim, time_function

def penneys_game(path, ngames: int, seed = 0) -> None:
    simulation = sim(ngames, seed)
    db_path = make_database(simulation, path)
    heatmap(db_path)

    return 

if __name__ == '__main__':
    time_function(penneys_game)('data/penney.db', 100, 0)