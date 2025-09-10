from dataclasses import dataclass


@dataclass
class Habit:
    id: int
    name: str
    description: str
    schedule_type: str  # 'daily' or 'weekly'
    goal: str
    expected_frequency: int
    start_date: str
    end_date: str = None


@dataclass
class Completion:
    id: int
    habit_id: int
    date: str
    timestamp: str
