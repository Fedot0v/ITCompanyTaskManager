import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, UpdateView
)

from tasks.form import WorkerCreateForm
from tasks.models import (
    Task,
    TaskType,
    Worker
)


@login_required
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


class TaskAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if not request.user in task.assignees.all():
            return HttpResponseForbidden("You don't have access to this task.")
        return super().dispatch(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/all_tasks_list.html"
    paginate_by = 5


class UserTaskListView(TaskListView):
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/tasks_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_types'] = TaskType.objects.all()
        context['workers'] = Worker.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

    def get_queryset(self):
        return Task.objects.select_related('task_type').prefetch_related('assignees')


class TaskUpdateView(TaskAccessMixin, UpdateView):
    model = Task
    fields = "__all__"
    template_name = "tasks/task_update.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_types"] = TaskType.objects.all()
        context["workers"] = Worker.objects.all()
        context['assignees'] = self.object.assignees.values_list('id', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.POST.get('status')
        if new_status is not None:
            task.is_completed = new_status == 'True'
            task.save()
        return redirect('tasks:tasks-detail', pk=task.pk)

    def get_success_url(self):
        return reverse_lazy("tasks:tasks-detail", kwargs={"pk": self.object.pk})


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    context_object_name = "tasks_types"
    template_name = "tasks/tasktype_list.html"
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/tasktype_form.html"


class WorkerCreateView(CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("login")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "tasks/workers_list.html"
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"
    context_object_name = "worker"


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerCreateForm
    context_object_name = "worker"
