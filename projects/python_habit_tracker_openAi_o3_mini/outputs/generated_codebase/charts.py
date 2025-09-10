import matplotlib.pyplot as plt
from db import get_completions_for_habit
import datetime


def plot_habit_progress(habit_id):
    # Retrieve completions for the habit
    completions = get_completions_for_habit(habit_id)
    dates = [comp['date'] for comp in completions]

    # Count completions per date
    date_counts = {}
    for d in dates:
        date_counts[d] = date_counts.get(d, 0) + 1

    # Sort the dates
    sorted_dates = sorted(date_counts.keys(), key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    counts = [date_counts[date] for date in sorted_dates]

    plt.figure(figsize=(10, 5))
    plt.bar(sorted_dates, counts)
    plt.xlabel('Date')
    plt.ylabel('Number of Completions')
    plt.title(f'Habit {habit_id} Progress')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
