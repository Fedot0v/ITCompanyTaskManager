from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class DeadlineMixin(models.Model):
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def days_remaining(self):
        today = timezone.now().date()
        deadline_date = self.deadline.date()
        if deadline_date >= today:
            return (deadline_date - today).days
        elif deadline_date == today:
            return 0
        else:
            return "Deadline is overdue"

    def status(self):
        if self.is_completed:
            return "Completed"
        elif self.days_remaining() == "Deadline is overdue":
            return "Overdue"
        else:
            return "Pending"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

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


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(Worker, related_name="teams")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_teams"
    )

    def __str__(self):
        return self.name


class Project(DeadlineMixin, models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    teams = models.ManyToManyField(
        Team,
        related_name="projects"
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name='assigned_projects',
        related_query_name='assigned_projects'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )

    def __str__(self):
        return self.name


class Task(DeadlineMixin, models.Model):
    PRIORITY_CHOICES = {
        "urgent": "Urgent",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
    }
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateTimeField()
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES,
        default="low"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="task")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new_task = self.pk is None
        super().save(*args, **kwargs)

        if is_new_task and self.team:
            users_in_team = self.team.members.all()
            for user in users_in_team:
                if self not in user.task.all():
                    user.task.add(self)
