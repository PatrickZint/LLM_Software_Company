import numpy as np
from config import Config
from numerical_integration import euler_integration, rk4_integration

class PhysicsEngine:
    """Handles the physics simulation using Newton's law of gravitation and numerical integration."""

    def __init__(self, integration_method=None):
        # Initialize bodies using configuration
        self.G = Config.G
        self.dt = Config.TIME_STEP
        self.integration_method = integration_method if integration_method else Config.INTEGRATION_METHOD

        # Initialize two bodies. Each body carries a 'trail' for rendering paths.
        self.bodies = [
            {
                'mass': Config.BODY1['mass'],
                'pos': Config.BODY1['pos'].copy(),
                'vel': Config.BODY1['vel'].copy(),
                'trail': [],
                'max_trail_length': Config.MAX_TRAIL_LENGTH
            },
            {
                'mass': Config.BODY2['mass'],
                'pos': Config.BODY2['pos'].copy(),
                'vel': Config.BODY2['vel'].copy(),
                'trail': [],
                'max_trail_length': Config.MAX_TRAIL_LENGTH
            }
        ]

    def set_integration_method(self, method):
        """Switch the integration method on the fly."""
        if method in ['euler', 'rk4']:
            self.integration_method = method
        else:
            raise ValueError('Unknown integration method: choose "euler" or "rk4"')

    def step(self):
        """Simulate a single time step using the selected numerical integration method."""
        if self.integration_method == 'euler':
            self.bodies = euler_integration(self.bodies, self.dt, self.G)
        elif self.integration_method == 'rk4':
            self.bodies = rk4_integration(self.bodies, self.dt, self.G)
        else:
            raise ValueError('Invalid integration method set in PhysicsEngine')

    def get_state(self):
        """Return the current state of the simulation (bodies data)."""
        return self.bodies

    def reset(self):
        """Reset the simulation to initial state as defined in config."""
        self.__init__()
