import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, UpdateView
)

from tasks.form import WorkerCreateForm, WorkerSearchForm, TaskSearchForm, ProjectCreateForm
from tasks.models import (
    Task,
    TaskType,
    Worker, Position, Project
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


class AccessMixin:
    model = None  # Model should be defined in the subclass

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user in obj.assignees.all() and not request.user == obj.creator:
            return HttpResponseForbidden("You don't have access to this object.")
        return super().dispatch(request, *args, **kwargs)


class TaskAccessMixin(AccessMixin):
    model = Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/all_tasks_list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-deadline')
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data["name"]
            assignees = form.cleaned_data["assignees"]
            tasktype = form.cleaned_data["tasktype"]
            status = form.cleaned_data["status"]

            if name:
                queryset = queryset.filter(name__icontains=name)
            if assignees:
                queryset = queryset.filter(assignees__in=assignees).distinct()
            if tasktype:
                queryset = queryset.filter(task_type=tasktype)
            if status == 'pending':
                queryset = queryset.filter(is_completed=False, deadline__gte=timezone.now())
            elif status == 'completed':
                queryset = queryset.filter(is_completed=True)
            elif status == 'overdue':
                queryset = queryset.filter(deadline__lt=timezone.now(), is_completed=False)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        assignees = self.request.GET.getlist("assignees")  # Use getlist for multiple selections
        tasktype = self.request.GET.get("tasktype", "")
        status = self.request.GET.get("status", "")

        # Make sure to convert assignees and tasktype to the appropriate types if needed
        context['search_form'] = TaskSearchForm(initial={
            "name": name,
            "assignees": assignees,
            # This might need to be adjusted based on how ModelMultipleChoiceField handles input
            "tasktype": tasktype,
            "status": status
        })
        return context


class UserTaskListView(TaskListView):
    template_name = "tasks/tasks_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(assignees=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        tasktype = self.request.GET.get("tasktype", "")
        status = self.request.GET.get("status", "")

        context['search_form'] = TaskSearchForm(initial={
            "name": name,
            "tasktype": tasktype,
            "status": status
        })
        return context


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

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    context_object_name = "tasks_types"
    template_name = "tasks/tasktype_list.html"
    paginate_by = 4


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    success_url = reverse_lazy("tasks:taskstype-list")
    template_name = "tasks/tasktype_form.html"
    fields = ["name"]


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

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username", "")
        last_name = self.request.GET.get("last_name", "")

        if username:
            queryset = queryset.filter(username__icontains=username)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = WorkerSearchForm(initial={
            "username": username,
            "last_name": last_name,
        })
        return context


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"
    context_object_name = "worker"


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "email", "position"]
    template_name = "tasks/worker_update.html"
    context_object_name = "worker"

    def get_success_url(self):
        return reverse_lazy("tasks:worker-detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["positions"] = Position.objects.all()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj:
            raise PermissionDenied
        return obj


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = "projects"
    template_name = "tasks/projects_list.html"
    paginate_by = 5


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "tasks/project_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = Worker.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:projects-detail", kwargs={"pk": self.object.pk})


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = "project"
    template_name = "tasks/project_detail.html"


class ProjectAccessMixin(AccessMixin):
    model = Project


class ProjectUpdateView(ProjectAccessMixin, LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "tasks/project_update.html"
    context_object_name = "project"

    def get_success_url(self):
        return reverse_lazy("tasks:projects-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = Worker.objects.all()
        return context
