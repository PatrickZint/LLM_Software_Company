import csv


def export_csv(logs, output_file):
    # logs is expected to be a list of tuples: (timestamp, source_path, destination_path, rule_applied)
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(["Timestamp", "Source Path", "Destination Path", "Rule Applied"])
        # Write log rows
        for log in logs:
            writer.writerow(log)
