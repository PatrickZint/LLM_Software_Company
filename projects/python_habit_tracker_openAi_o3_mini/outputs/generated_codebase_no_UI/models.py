from dataclasses import dataclass

@dataclass
class Habit:
    id: int = None
    title: str = ""
    description: str = ""
    goal: str = ""
    schedule: str = ""
    start_date: str = ""
    end_date: str = None
    category: str = ""


@dataclass
class HabitLog:
    id: int = None
    habit_id: int = None
    log_date: str = ""
    status: str = ""  # e.g., 'completed' or 'skipped'
    notes: str = ""
