from retail_simulator.daemon.simulation import Simulation

def run():
    simulation = Simulation(parameters_file_path="./src/retail_simulator/config/parameters.json")
    simulation.run(days=1)
    simulation.run(days=2)
    simulation.run(days=1)
    simulation.run(days=3)

if __name__ == "__main__":
    run()
