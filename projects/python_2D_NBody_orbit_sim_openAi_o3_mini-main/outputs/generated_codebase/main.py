import sys
import pygame
import threading
import time

from config import load_config
from physics_engine import PhysicsEngine
from integration_strategies import EulerIntegration, VerletIntegration, RungeKuttaIntegration
from visualization import SimulationWindow
from controller import Controller
from logging_module import SimulationLogger


def select_integration_strategy(strategy_name):
    if strategy_name.lower() == 'euler':
        return EulerIntegration()
    elif strategy_name.lower() == 'verlet':
        return VerletIntegration()
    elif strategy_name.lower() == 'rungekutta':
        return RungeKuttaIntegration()
    else:
        raise ValueError(f"Unknown integration strategy: {strategy_name}")


def main():
    # Load and validate configuration
    config = load_config('config.json')

    # Select integration method based on config
    integration_method = select_integration_strategy(config.get('integration_method', 'euler'))

    # Initialize Logger
    sim_logger = SimulationLogger(config.get('log_file', 'simulation_log.json'))

    # Initialize Physics Engine with initial bodies and parameters
    physics = PhysicsEngine(
        bodies=config.get('bodies', []),
        time_step=config.get('time_step', 0.01),
        gravitational_constant=config.get('gravitational_constant', 6.67430e-11),
        integration_strategy=integration_method,
        logger=sim_logger
    )

    # Initialize Visualization
    pygame.init()
    window_size = config.get('window_size', [800, 600])
    simulation_window = SimulationWindow(window_size)

    # Initialize Controller
    controller = Controller(physics, simulation_window)

    # Start logger thread
    sim_logger.start()

    # Start simulation in a separate thread
    simulation_thread = threading.Thread(target=controller.run, daemon=True)
    simulation_thread.start()

    try:
        # Main loop for visualization (View)
        while True:
            simulation_window.handle_events(controller)
            simulation_window.render(physics.get_state())
            pygame.display.flip()
            time.sleep(1/30)  # Aim for 30 FPS
    except KeyboardInterrupt:
        controller.stop()
    finally:
        pygame.quit()
        sim_logger.stop()
        simulation_thread.join()


if __name__ == '__main__':
    main()