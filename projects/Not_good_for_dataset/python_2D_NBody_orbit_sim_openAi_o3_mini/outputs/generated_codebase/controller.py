import threading
import time


class Controller:
    def __init__(self, physics_engine, simulation_window):
        self.physics_engine = physics_engine
        self.simulation_window = simulation_window
        self._running = False
        self.lock = threading.Lock()

    def run(self):
        self._running = True
        # Run the simulation loop in this thread
        while self._running:
            self.physics_engine.update()
            time.sleep(self.physics_engine.time_step)  # Regulate simulation speed

    def pause(self):
        with self.lock:
            self.physics_engine.pause()
            self._running = False

    def resume(self):
        with self.lock:
            if not self._running:
                self.physics_engine.resume()
                # Restart the simulation loop in a new thread
                threading.Thread(target=self.run, daemon=True).start()
                self._running = True

    def stop(self):
        with self.lock:
            self.physics_engine.stop()
            self._running = False

    def is_running(self):
        return self._running

    # Methods to dispatch runtime events e.g., add/remove body
    def add_body(self, body_config):
        self.physics_engine.add_body(body_config)

    def remove_body(self, body_id):
        self.physics_engine.remove_body(body_id)
