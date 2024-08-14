from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import (
    Task,
    Team,
    TaskType,
    Project,
    Position
)


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Test Position")
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            position=cls.position,
            password="testpassword"
        )
        cls.team = Team.objects.create(name='Test Team', created_by=cls.user)
        cls.task_type = TaskType.objects.create(name='Test TaskType')
        cls.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            deadline=timezone.now() + timezone.timedelta(days=5),
            team=cls.team,
            created_by=cls.user
        )
        cls.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            deadline=timezone.now() + timezone.timedelta(days=5),
            priority='low',
            task_type=cls.task_type,
            project=cls.project,
            team=cls.team
        )


class TaskListViewTestCase(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("tasks:tasks-list")

    def test_task_list_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/all_tasks_list.html")
        self.assertContains(response, "Test Task")

    def test_task_list_view_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TaskCreateViewTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("tasks:tasks-form")

    def test_task_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tasks_form.html")
        self.assertContains(response, "Test Task")
