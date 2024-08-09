from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        db_constraint=False,
        default=1
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.position}"


class Task(models.Model):
    PRIORITY_CHOICES = {
        "urgent": "Urgent",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
    }
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES,
        default="low"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="task")

    def __str__(self):
        return self.name

    def days_remaining(self):
        today = timezone.now().date()
        deadline_date = self.deadline.date()
        if deadline_date >= today:
            return (deadline_date - today).days
        elif deadline_date == today:
            return 0
        else:
            return "Deadline is overdue"
