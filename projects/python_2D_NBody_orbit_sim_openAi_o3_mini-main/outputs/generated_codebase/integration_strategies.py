from abc import ABC, abstractmethod
import math


class IntegrationStrategy(ABC):
    @abstractmethod
    def step(self, bodies, forces, time_step, G):
        pass


class EulerIntegration(IntegrationStrategy):
    def step(self, bodies, forces, time_step, G):
        # Simple Euler integration
        for body in bodies.values():
            # Sum forces on this body
            total_force = [0.0, 0.0]
            for other_id, other_body in bodies.items():
                if other_id == body.id:
                    continue
                # Use the precomputed forces if available
                key = (body.id, other_id)
                if key in forces:
                    f = forces[key]
                    total_force[0] += f[0]
                    total_force[1] += f[1]
            # Acceleration = force / mass
            ax = total_force[0] / body.mass
            ay = total_force[1] / body.mass
            # Update velocity
            body.velocity[0] += ax * time_step
            body.velocity[1] += ay * time_step
            # Update position
            body.position[0] += body.velocity[0] * time_step
            body.position[1] += body.velocity[1] * time_step


class VerletIntegration(IntegrationStrategy):
    def __init__(self):
        self.previous_positions = {}

    def step(self, bodies, forces, time_step, G):
        # Verlet integration method
        for body in bodies.values():
            # Save current position
            current_position = body.position.copy()
            # Sum forces
            total_force = [0.0, 0.0]
            for other_id, other_body in bodies.items():
                if other_id == body.id:
                    continue
                key = (body.id, other_id)
                if key in forces:
                    f = forces[key]
                    total_force[0] += f[0]
                    total_force[1] += f[1]
            # Acceleration = force / mass
            ax = total_force[0] / body.mass
            ay = total_force[1] / body.mass
            if body.id not in self.previous_positions:
                # For the first time step, use Euler to initialize
                new_x = body.position[0] + body.velocity[0] * time_step + 0.5 * ax * time_step * time_step
                new_y = body.position[1] + body.velocity[1] * time_step + 0.5 * ay * time_step * time_step
            else:
                new_x = 2 * body.position[0] - self.previous_positions[body.id][0] + ax * time_step * time_step
                new_y = 2 * body.position[1] - self.previous_positions[body.id][1] + ay * time_step * time_step
            # Update velocity estimate
            body.velocity[0] = (new_x - self.previous_positions.get(body.id, body.position)[0]) / (2 * time_step)
            body.velocity[1] = (new_y - self.previous_positions.get(body.id, body.position)[1]) / (2 * time_step)

            self.previous_positions[body.id] = current_position
            body.position[0] = new_x
            body.position[1] = new_y


class RungeKuttaIntegration(IntegrationStrategy):
    def step(self, bodies, forces, time_step, G):
        # A simplified RK4 integration for updating positions and velocities
        # Note: In a full implementation, you would calculate intermediate slopes
        for body in bodies.values():
            # Sum forces on body
            total_force = [0.0, 0.0]
            for other_id, other_body in bodies.items():
                if other_id == body.id:
                    continue
                key = (body.id, other_id)
                if key in forces:
                    f = forces[key]
                    total_force[0] += f[0]
                    total_force[1] += f[1]
            ax = total_force[0] / body.mass
            ay = total_force[1] / body.mass
            # RK4 intermediate calculations - simplified version
            k1_vx = ax
            k1_vy = ay
            k1_x = body.velocity[0]
            k1_y = body.velocity[1]

            k2_vx = ax  # For simplicity, using same acceleration
            k2_vy = ay
            k2_x = body.velocity[0] + 0.5 * k1_vx * time_step
            k2_y = body.velocity[1] + 0.5 * k1_vy * time_step

            k3_vx = ax
            k3_vy = ay
            k3_x = body.velocity[0] + 0.5 * k2_vx * time_step
            k3_y = body.velocity[1] + 0.5 * k2_vy * time_step

            k4_vx = ax
            k4_vy = ay
            k4_x = body.velocity[0] + k3_vx * time_step
            k4_y = body.velocity[1] + k3_vy * time_step

            body.velocity[0] += (time_step / 6) * (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx)
            body.velocity[1] += (time_step / 6) * (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy)
            
            body.position[0] += (time_step / 6) * (k1_x + 2*k2_x + 2*k3_x + k4_x)
            body.position[1] += (time_step / 6) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
