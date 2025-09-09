from simulation import SimulationCore
from gui import GUI
import time

if __name__ == '__main__':
    # Initialize simulation core and start simulation thread
    simulation = SimulationCore()
    simulation.start()

    # Initialize and run the GUI
    gui = GUI(simulation)
    try:
        gui.run()
    except KeyboardInterrupt:
        pass
    finally:
        simulation.stop()
        # Optional: Export simulation log data
        simulation.logger.export_to_json('simulation_log.json')
        print('Simulation ended. Log exported to simulation_log.json')
