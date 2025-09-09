import json
import threading
import time


class SimulationLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.entries = []
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def log(self, simulation_time, state, forces):
        entry = {
            'time': simulation_time,
            'state': state,
            'forces': {f'{k[0]}-{k[1]}': v for k, v in forces.items()}
        }
        with self.lock:
            self.entries.append(entry)

    def _write_logs(self):
        while self.running:
            time.sleep(1)  # Write every second; adjust as needed
            with self.lock:
                if self.entries:
                    try:
                        with open(self.log_file, 'a') as f:
                            for entry in self.entries:
                                f.write(json.dumps(entry) + '\n')
                        self.entries = []
                    except Exception as e:
                        print(f"Error writing log: {e}")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._write_logs, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
