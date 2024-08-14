from django.test import TestCase
from django.utils import timezone

from tasks.form import WorkerCreateForm, TaskSearchForm
from tasks.models import Task, Position, TaskType
from django.contrib.auth import get_user_model


class WorkerCreateFormTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Test Position")

    def test_form_valid(self):
        form_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@mail.com",
            "position": self.position.pk,
            "password1": "testpassword",
            "password2": "testpassword"
        }
        form = WorkerCreateForm(form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'position': self.position.pk,
            'password1': 'testpassword',
            'password2': 'differentpassword'
        }
        form = WorkerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class TaskSearchFormTest(TestCase):

    def setUp(self):
        self.task_type = TaskType.objects.create(name="Test Task Type")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Task",
            deadline=timezone.now() + timezone.timedelta(days=5),
            priority="low",
            task_type=self.task_type,
        )

    def test_search_form_valid(self):
        form_data = {
            "name": "Test Task",
        }
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_invalid(self):
        form_data = {}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
