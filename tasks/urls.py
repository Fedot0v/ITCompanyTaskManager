from django.urls import path

from .views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskTypeCreateView,
    TaskTypeListView,
    WorkerCreateView,
    TaskDetailView,
    UserTaskListView, WorkerDetailView
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("mytasks/", UserTaskListView.as_view(), name="mytasks-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="tasks-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="tasks-form"),
    path("tasktype/create/", TaskTypeCreateView.as_view(), name="tasktype-form"),
    path("taskstype/", TaskTypeListView.as_view(), name="taskstype-list"),
    path("signup/", WorkerCreateView.as_view(), name="signup"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
]
