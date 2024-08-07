from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

from tasks.models import Task


def index(request):
    """View function for the home page of the site."""
    return render(request, "tasks/index.html")


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    paginated_by = 5


class TaskCreateView(CreateView):
    model = Task
    fields = "__all__"
