import threading
import math


class CelestialBody:
    def __init__(self, id, position, velocity, mass):
        self.id = id
        self.position = position  # [x, y]
        self.velocity = velocity  # [vx, vy]
        self.mass = mass

    def to_dict(self):
        return {
            'id': self.id,
            'position': self.position,
            'velocity': self.velocity,
            'mass': self.mass
        }


class PhysicsEngine:
    def __init__(self, bodies, time_step, gravitational_constant, integration_strategy, logger):
        # Convert each body config dict to a CelestialBody instance
        self.bodies = {}
        for body in bodies:
            b = CelestialBody(
                id=body.get('id'),
                position=body.get('position', [0.0, 0.0]),
                velocity=body.get('velocity', [0.0, 0.0]),
                mass=body.get('mass', 1.0)
            )
            self.bodies[b.id] = b

        self.time_step = time_step
        self.G = gravitational_constant
        self.integration_strategy = integration_strategy
        self.lock = threading.Lock()
        self.running = False
        self.logger = logger
        self.current_time = 0.0

    def add_body(self, body_config):
        with self.lock:
            b = CelestialBody(
                id=body_config.get('id'),
                position=body_config.get('position', [0.0, 0.0]),
                velocity=body_config.get('velocity', [0.0, 0.0]),
                mass=body_config.get('mass', 1.0)
            )
            self.bodies[b.id] = b

    def remove_body(self, body_id):
        with self.lock:
            if body_id in self.bodies:
                del self.bodies[body_id]

    def compute_forces(self):
        """
        Computes gravitational forces between every pair of bodies.
        Returns a dictionary with key as tuple (id1, id2) and value as force vector [fx, fy].
        """
        forces = {}
        bodies_list = list(self.bodies.values())
        n = len(bodies_list)

        for i in range(n):
            for j in range(i + 1, n):
                b1 = bodies_list[i]
                b2 = bodies_list[j]
                dx = b2.position[0] - b1.position[0]
                dy = b2.position[1] - b1.position[1]
                distance_sq = dx * dx + dy * dy + 1e-10  # Avoid division by zero
                distance = math.sqrt(distance_sq)
                force_magnitude = self.G * b1.mass * b2.mass / distance_sq
                # Force vector components
                fx = force_magnitude * dx / distance
                fy = force_magnitude * dy / distance
                forces[(b1.id, b2.id)] = [fx, fy]
                forces[(b2.id, b1.id)] = [-fx, -fy]
        return forces

    def update(self):
        """
        Advances the simulation by one time step using the configured integration strategy.
        """
        with self.lock:
            forces = self.compute_forces()
            # Delegate integration step to the chosen strategy
            self.integration_strategy.step(self.bodies, forces, self.time_step, self.G)
            self.current_time += self.time_step
            if self.logger is not None:
                # Log current state
                state = self.get_state()
                self.logger.log(self.current_time, state, forces)

    def get_state(self):
        """
        Returns the current state of the simulation (all bodies as dictionaries).
        """
        with self.lock:
            return {bid: body.to_dict() for bid, body in self.bodies.items()}

    def run(self):
        self.running = True
        while self.running:
            self.update()

    def pause(self):
        self.running = False

    def resume(self):
        if not self.running:
            self.running = True

    def stop(self):
        self.running = False
