import json
import os


def load_config(filename):
    """
    Loads simulation configuration from a JSON file and validates input values.

    Required keys:
      - bodies: list of celestial bodies with their properties
      - time_step: positive float
      - gravitational_constant: float
      - integration_method: 'euler', 'verlet', or 'rungekutta'
      - window_size: [width, height]

    Returns a dictionary with configuration.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Configuration file {filename} not found.")

    with open(filename, 'r') as f:
        config = json.load(f)

    # Validate time_step
    if config.get('time_step', 0) <= 0:
        raise ValueError("time_step must be a positive float.")

    # Validate gravitational constant (should be positive)
    if config.get('gravitational_constant', 0) <= 0:
        raise ValueError("gravitational_constant must be a positive float.")

    # Validate bodies
    for body in config.get('bodies', []):
        if body.get('mass', -1) < 0:
            raise ValueError(f"Body {body.get('id', 'unknown')} has invalid mass.")

    return config