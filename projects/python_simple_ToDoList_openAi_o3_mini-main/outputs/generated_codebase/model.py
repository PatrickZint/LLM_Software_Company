import datetime


class Task:
    def __init__(self, description, due_date=None, priority="Normal", category="General", status="pending"):
        self.description = description
        self.due_date = due_date  # Can be a string or datetime
        self.priority = priority
        self.category = category
        self.status = status

    def mark_complete(self):
        self.status = "completed"

    def update(self, description=None, due_date=None, priority=None, category=None, status=None):
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        if priority is not None:
            self.priority = priority
        if category is not None:
            self.category = category
        if status is not None:
            self.status = status

    def to_dict(self):
        return {
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "category": self.category,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            description=data.get("description"),
            due_date=data.get("due_date"),
            priority=data.get("priority", "Normal"),
            category=data.get("category", "General"),
            status=data.get("status", "pending")
        )


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def update_task(self, index, task):
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def get_tasks(self):
        return self.tasks

    def to_list(self):
        return [task.to_dict() for task in self.tasks]

    def load_from_list(self, tasks_list):
        self.tasks = [Task.from_dict(item) for item in tasks_list]
