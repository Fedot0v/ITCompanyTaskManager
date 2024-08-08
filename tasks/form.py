from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Worker


class WorkerCreateForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email"
        )
