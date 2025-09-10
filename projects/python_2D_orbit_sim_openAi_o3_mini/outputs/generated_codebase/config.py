import numpy as np

# Configuration Manager for simulation parameters

class Config:
    # Gravitational constant in SI units: m^3 kg^-1 s^-2
    G = 6.67430e-11

    # Default time step (seconds)
    TIME_STEP = 60.0

    # Simulation mode: 'real-time' or 'accelerated'
    MODE = 'real-time'

    # Integration method: 'euler' for fast/less accurate, 'rk4' for accurate simulation
    INTEGRATION_METHOD = 'rk4'

    # Default simulation window size (for GUI rendering)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    # Colors (RGB)
    BG_COLOR = (0, 0, 0)
    BODY_COLOR = (255, 255, 255)
    TRAIL_COLOR = (0, 255, 0)
    TEXT_COLOR = (255, 255, 0)

    # Default bodies configuration. Each body is represented as a dict:
    # 'mass': mass in kg, 'pos': np.array([x, y]) in meters, 'vel': np.array([vx, vy]) in m/s.
    BODY1 = {
        'mass': 5.972e24,  # Earth mass
        'pos': np.array([0.0, 0.0]),
        'vel': np.array([0.0, 0.0])
    }

    BODY2 = {
        'mass': 7.348e22,  # Moon mass
        'pos': np.array([384400000.0, 0.0]),  # distance from Earth
        'vel': np.array([0.0, 1022.0])  # orbital speed of the Moon around Earth
    }

    # Scaling factor for rendering (to convert meters to pixels)
    SCALE = 1e-6

    # Maximum length of trail to display
    MAX_TRAIL_LENGTH = 100
