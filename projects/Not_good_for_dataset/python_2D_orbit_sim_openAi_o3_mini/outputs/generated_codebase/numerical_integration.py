import numpy as np

def euler_integration(bodies, dt, G):
    """Perform one integration step using Euler's method.

    bodies: list of dicts, each with keys 'mass', 'pos' (np.array), 'vel' (np.array)
    dt: time step
    G: gravitational constant

    Returns new state of bodies.
    """
    # Calculate accelerations for two-body problem
    b1, b2 = bodies[0], bodies[1]
    r_vec = b2['pos'] - b1['pos']
    r = np.linalg.norm(r_vec) + 1e-10  # avoid divide by zero
    direction = r_vec / r

    # acceleration on body1 due to body2
    a1 = G * b2['mass'] / (r ** 2) * direction
    # acceleration on body2 due to body1
    a2 = G * b1['mass'] / (r ** 2) * (-direction)

    new_bodies = []
    for body, accel in zip(bodies, [a1, a2]):
        new_vel = body['vel'] + accel * dt
        new_pos = body['pos'] + body['vel'] * dt
        # Update trail: accumulate past positions
        trail = body.get('trail', [])
        trail.append(new_pos.copy())
        if len(trail) > body.get('max_trail_length', 100):
            trail.pop(0)
        new_body = {
            'mass': body['mass'],
            'pos': new_pos,
            'vel': new_vel,
            'trail': trail,
            'max_trail_length': body.get('max_trail_length', 100)
        }
        new_bodies.append(new_body)

    return new_bodies


def rk4_integration(bodies, dt, G):
    """Perform one integration step using fourth-order Runge-Kutta.

    The state for each body is defined as y = [x, y, vx, vy].
    """
    # For two bodies
    b1, b2 = bodies[0], bodies[1]

    def deriv(y1, y2):
        """Compute derivatives for two bodies given state y1 and y2.
           y = [x, y, vx, vy]
        """
        pos1 = y1[0:2]
        vel1 = y1[2:4]
        pos2 = y2[0:2]
        vel2 = y2[2:4]

        r_vec = pos2 - pos1
        r = np.linalg.norm(r_vec) + 1e-10
        direction = r_vec / r
        # accelerations
        a1 = G * b2['mass'] / (r**2) * direction
        a2 = G * b1['mass'] / (r**2) * (-direction)

        return np.concatenate([vel1, a1]), np.concatenate([vel2, a2])

    # Prepare state vectors
    y1 = np.concatenate([b1['pos'], b1['vel']])
    y2 = np.concatenate([b2['pos'], b2['vel']])

    k1_y1, k1_y2 = deriv(y1, y2)
    k2_y1, k2_y2 = deriv(y1 + 0.5 * dt * k1_y1, y2 + 0.5 * dt * k1_y2)
    k3_y1, k3_y2 = deriv(y1 + 0.5 * dt * k2_y1, y2 + 0.5 * dt * k2_y2)
    k4_y1, k4_y2 = deriv(y1 + dt * k3_y1, y2 + dt * k3_y2)

    y1_new = y1 + (dt / 6.0) * (k1_y1 + 2 * k2_y1 + 2 * k3_y1 + k4_y1)
    y2_new = y2 + (dt / 6.0) * (k1_y2 + 2 * k2_y2 + 2 * k3_y2 + k4_y2)

    # Update trails
    trail1 = b1.get('trail', [])
    trail2 = b2.get('trail', [])
    trail1.append(y1_new[0:2].copy())
    trail2.append(y2_new[0:2].copy())
    if len(trail1) > b1.get('max_trail_length', 100):
        trail1.pop(0)
    if len(trail2) > b2.get('max_trail_length', 100):
        trail2.pop(0)

    new_b1 = {
        'mass': b1['mass'],
        'pos': y1_new[0:2],
        'vel': y1_new[2:4],
        'trail': trail1,
        'max_trail_length': b1.get('max_trail_length', 100)
    }
    new_b2 = {
        'mass': b2['mass'],
        'pos': y2_new[0:2],
        'vel': y2_new[2:4],
        'trail': trail2,
        'max_trail_length': b2.get('max_trail_length', 100)
    }

    return [new_b1, new_b2]
