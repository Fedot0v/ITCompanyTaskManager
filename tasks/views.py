from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

from tasks.models import Task, TaskType


def index(request):
    """View function for the home page of the site."""
    #user = request.user
    #num_tasks = Task.objects.filter(user=user).count()  # Фільтруємо за користувачем
    #num_of_available_tasks = Task.objects.filter(user=user, is_completed=False).count()
    #num_of_completed_tasks = Task.objects.filter(user=user, is_completed=True).count()
    num_tasks = Task.objects.filter().count()  # Фільтруємо за користувачем
    num_of_available_tasks = Task.objects.filter(is_completed=False).count()
    num_of_completed_tasks = Task.objects.filter(is_completed=True).count()
    context = {
        "num_tasks": num_tasks,
        "num_of_available_tasks": num_of_available_tasks,
        "num_of_completed_tasks": num_of_completed_tasks,
    }
    return render(request, 'tasks/index.html', context)


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    paginated_by = 5


class TaskCreateView(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/tasks_form.html"


class TaskTypeListView(ListView):
    model = TaskType
    context_object_name = "task_types"


class TaskTypeCreateView(CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/tasktype_form.html"

