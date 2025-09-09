import unittest
from model import Task, TaskManager


class TestTask(unittest.TestCase):
    def test_mark_complete(self):
        task = Task("Test Task")
        self.assertEqual(task.status, "pending")
        task.mark_complete()
        self.assertEqual(task.status, "completed")

    def test_update(self):
        task = Task("Old Task")
        task.update(description="New Task")
        self.assertEqual(task.description, "New Task")

    def test_to_from_dict(self):
        task = Task("Sample Task", due_date="2023-10-10", priority="High", category="Work", status="pending")
        task_dict = task.to_dict()
        new_task = Task.from_dict(task_dict)
        self.assertEqual(new_task.description, "Sample Task")
        self.assertEqual(new_task.due_date, "2023-10-10")
        self.assertEqual(new_task.priority, "High")
        self.assertEqual(new_task.category, "Work")
        self.assertEqual(new_task.status, "pending")


class TestTaskManager(unittest.TestCase):
    def test_add_and_delete_task(self):
        manager = TaskManager()
        task1 = Task("Task 1")
        manager.add_task(task1)
        self.assertEqual(len(manager.get_tasks()), 1)
        manager.delete_task(0)
        self.assertEqual(len(manager.get_tasks()), 0)

    def test_update_task(self):
        manager = TaskManager()
        task1 = Task("Task 1")
        manager.add_task(task1)
        task1_updated = Task("Task 1 Updated")
        manager.update_task(0, task1_updated)
        self.assertEqual(manager.get_tasks()[0].description, "Task 1 Updated")


if __name__ == '__main__':
    unittest.main()
