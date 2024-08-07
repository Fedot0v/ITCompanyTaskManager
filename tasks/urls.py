from django.urls import path

from .views import (
    index,
    TaskListView,
    TaskCreateView
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("tasks/<int:pk>/create/", TaskCreateView.as_view(), name="tasks-form"),
]
