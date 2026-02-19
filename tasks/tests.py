from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from .models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        task = Task.objects.create(
            task_name="test task", task_deadline=now(), recurring=False, preparation=False
        )

    def test_task_name(self):
        task = Task.objects.create(
            task_name="Task 1", task_deadline=now(), recurring=False, preparation=False
        )
        self.assertEqual("Task 1", task.task_name)

    def test_is_recurring(self):
        task = Task.objects.create(
            task_name="Task 1", task_deadline=now(), recurring=False, preparation=False
        )
        self.assertEqual(False, task.recurring)

    def test_needs_prep(self):
        task = Task.objects.create(
            task_name="Task 1", task_deadline=now(), recurring=False, preparation=False
        )
        self.assertEqual(False, task.preparation)

    def test_prep_amount(self):
        task = Task.objects.create(
            task_name="Task 1",
            task_deadline=now(),
            recurring=False,
            preparation=False,
            how_much_prep="Medium",
        )
        self.assertEqual("Medium", task.how_much_prep)

    def test_priority_level(self):
        task = Task.objects.create(
            task_name="Task 1",
            task_deadline=now(),
            recurring=False,
            preparation=False,
            priority_level="Low",
        )
        self.assertEqual("Low", task.priority_level)


class TaskIndexViewTests(TestCase):
    @staticmethod
    def create_task(name, duedate, prep, recurring):
        return Task.objects.create(task_name=name, duedate=now(), prep=True, recurring=False)


def test_no_tasks(self):
    response = self.client.get(reverse("tasks:task-list"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No tasks available.")
    self.assertQuerysetEqual(response.context["tasks"], ["<Task: "])
