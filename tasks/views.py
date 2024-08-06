from django.shortcuts import render
from django.views.generic import ListView

from tasks.models import Task


def index(request):
    """View function for the home page of the site."""
    return render(request, "index.html")


class TaskListView(ListView):
    model = Task
    context_object_name = "task"
