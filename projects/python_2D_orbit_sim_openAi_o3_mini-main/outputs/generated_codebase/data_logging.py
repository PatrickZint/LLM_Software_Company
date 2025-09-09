import csv
import json

class DataLogger:
    """Manages simulation state logging and data export."""

    def __init__(self):
        # Use an in-memory buffer to store simulation states
        self.logs = []

    def log_state(self, time, bodies):
        """Log the simulation state for a given time stamp.
        bodies: list of dictionaries, each with keys: 'pos', 'vel', 'mass'
        """
        state = {
            'time': time,
            'bodies': [
                {
                    'mass': body['mass'],
                    'pos': body['pos'].tolist(),
                    'vel': body['vel'].tolist()
                } for body in bodies
            ]
        }
        self.logs.append(state)

    def export_to_csv(self, filename):
        """Exports logged data to CSV format."""
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['time', 'body', 'mass', 'pos_x', 'pos_y', 'vel_x', 'vel_y']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.logs:
                time_stamp = entry['time']
                for i, body in enumerate(entry['bodies']):
                    writer.writerow({
                        'time': time_stamp,
                        'body': f'body{i+1}',
                        'mass': body['mass'],
                        'pos_x': body['pos'][0],
                        'pos_y': body['pos'][1],
                        'vel_x': body['vel'][0],
                        'vel_y': body['vel'][1]
                    })

    def export_to_json(self, filename):
        """Exports logged data to JSON format."""
        with open(filename, 'w') as jsonfile:
            json.dump(self.logs, jsonfile, indent=4)
