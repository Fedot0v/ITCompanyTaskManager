from django.urls import path

from tasks.views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskTypeCreateView,
    TaskTypeListView,
    WorkerCreateView,
    TaskDetailView,
    UserTaskListView,
    WorkerDetailView,
    WorkerListView,
    TaskUpdateView,
    WorkerUpdateView,
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    TeamCreateView,
    TeamListView,
    TeamDeleteView,
    ProjectDeleteView,
    TaskTypeDeleteView,
    TaskDeleteView,
    TeamDetailView,
    TeamUpdateView,
    PositionCreateView
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("mytasks/", UserTaskListView.as_view(), name="mytasks-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="tasks-detail"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="tasks-update"
    ),
    path("tasks/create/", TaskCreateView.as_view(), name="tasks-form"),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="tasks-delete"
    ),
    path(
        "tasktype/create/",
        TaskTypeCreateView.as_view(),
        name="tasktype-form"
    ),
    path("taskstype/", TaskTypeListView.as_view(), name="taskstype-list"),
    path(
        "taskstype/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="taskstype-delete"
    ),
    path("signup/", WorkerCreateView.as_view(), name="signup"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
    path(
        "workers/<int:pk>",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="workers-update"
    ),
    path(
        "projects/", ProjectListView.as_view(),
        name="projects-list"
    ),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="projects-create"
    ),
    path(
        "projects/<int:pk>",
        ProjectDetailView.as_view(),
        name="projects-detail"
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="projects-update"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="projects-delete"
    ),
    path(
        "team/create/", TeamCreateView.as_view(), name="team-form"),
    path("teams/", TeamListView.as_view(), name="teams-list"),
    path(
        "teams/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="teams-delete"
    ),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="teams-detail"),
    path(
        "teams/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="teams-update"
    ),
    path(
        "position/create/",
        PositionCreateView.as_view(),
        name="position-form"
    ),
]
