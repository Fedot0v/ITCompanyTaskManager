from django.contrib import admin

from tasks.models import (
    Task,
    Project,
    Team,
    Worker,
    TaskType,
    Position
)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name", "description", "deadline", "priority", "task_type",
        "project", "team", "is_completed"
    )
    list_filter = ("priority", "task_type", "project", "team", "is_completed")
    search_fields = (
        "name", "description", "task_type__name", "project__name",
        "team__name"
    )
    ordering = ("-deadline",)
    filter_horizontal = ("assignees",)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date")
    list_filter = ("teams", "assignees")
    search_fields = ("name", "description")
    filter_horizontal = ("teams", "assignees")


class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by")
    search_fields = ("name", "created_by__username")
    filter_horizontal = ("members",)


class WorkerAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "position")
    list_filter = ("position",)
    search_fields = ("username", "first_name", "last_name", "position__name")


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Position, PositionAdmin)
