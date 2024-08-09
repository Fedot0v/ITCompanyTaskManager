import datetime

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

from tasks.form import WorkerCreateForm
from tasks.models import (
    Task,
    TaskType,
    Worker
)


def index(request):
    """View function for the home page of the site."""
    user = request.user
    if user.is_authenticated:
        num_tasks = Task.objects.filter(assignees=user).count()  # Filter by user
        num_of_available_tasks = Task.objects.filter(assignees=user, is_completed=False).count()
        num_of_completed_tasks = Task.objects.filter(assignees=user, is_completed=True).count()
    else:
        num_tasks = num_of_available_tasks = num_of_completed_tasks = 0
    # num_tasks = Task.objects.filter().count()
    # num_of_available_tasks = Task.objects.filter(is_completed=False).count()
    # num_of_completed_tasks = Task.objects.filter(is_completed=True).count()
    context = {
        "num_tasks": num_tasks,
        "num_of_available_tasks": num_of_available_tasks,
        "num_of_completed_tasks": num_of_completed_tasks,
    }
    return render(request, 'tasks/index.html', context)


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/all_tasks_list.html"
    paginate_by = 5


class UserTaskListView(TaskListView):
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class TaskCreateView(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/tasks_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_types'] = TaskType.objects.all()
        context['workers'] = Worker.objects.all()
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

    def get_queryset(self):
        return Task.objects.select_related('task_type').prefetch_related('assignees')


class TaskTypeListView(ListView):
    model = TaskType
    context_object_name = "tasks_types"
    template_name = "tasks/tasktype_list.html"
    paginate_by = 5


class TaskTypeCreateView(CreateView):
    model = TaskType
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/tasktype_form.html"


class WorkerCreateView(CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("login")


class WorkerListView(ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "tasks/workers_list.html"
    paginate_by = 5


class WorkerDetailView(DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"
    context_object_name = "worker"

