from django.test import TestCase
from django.utils import timezone
from tasks.models import Task, Team, TaskType, Project
from django.contrib.auth import get_user_model


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        cls.team = Team.objects.create(
            name="Test Team",
            created_by=cls.user,
        )
        cls.task_type = TaskType.objects.create(
            name="Test Task Type"
        )
        cls.project = Project.objects.create(
            name="Test Project",
            team=cls.team,
            deadline=timezone.now() + timezone.timedelta(days=5),
            created_by=cls.user,
        )
        cls.task = Task.objects.create(
            name="Test Task",
            description="Test Task",
            deadline=timezone.now() + timezone.timedelta(days=5),
            priority="low",
            task_type=cls.task_type,
            project=cls.project,
            team=cls.team
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_days_remaining(self):
        self.assertEqual(self.task.days_remaining(), 5)

    def test_task_completed_status(self):
        self.task.is_completed = True
        self.task.save()
        self.assertEqual(self.task.status(), "Completed")
