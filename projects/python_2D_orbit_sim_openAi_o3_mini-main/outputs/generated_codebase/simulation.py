import time
from threading import Thread, Event
from physics_engine import PhysicsEngine
from data_logging import DataLogger
from config import Config

class SimulationCore:
    """Encapsulates the simulation loop, time management, and logging."""

    def __init__(self):
        self.engine = PhysicsEngine()
        self.logger = DataLogger()
        self.time_elapsed = 0.0
        self.is_running = False
        self.is_paused = False
        self.dt = Config.TIME_STEP
        
        # Event to signal simulation loop to stop
        self._stop_event = Event()

    def start(self):
        """Start the simulation loop in a separate thread."""
        if not self.is_running:
            self.is_running = True
            self._stop_event.clear()
            self.thread = Thread(target=self._run_loop, daemon=True)
            self.thread.start()

    def _run_loop(self):
        while not self._stop_event.is_set():
            if not self.is_paused:
                # Perform one physics step
                self.engine.step()
                self.time_elapsed += self.dt
                # Log the state
                self.logger.log_state(self.time_elapsed, self.engine.get_state())
            time.sleep(0.01)  # sleep briefly to yield execution

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def reset(self):
        self.pause()
        self.engine.reset()
        self.time_elapsed = 0.0
        self.logger.logs = []
        self.resume()

    def stop(self):
        self._stop_event.set()
        self.is_running = False

    def get_state(self):
        """Expose current state for GUI rendering."""
        return self.engine.get_state()

    def get_time(self):
        return self.time_elapsed
