from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Worker, Position, Task, TaskType, Project, Team


class WorkerCreateForm(UserCreationForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all(), empty_label=None)

    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match")
        return password2


class WorkerSearchForm(forms.Form):
    username = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)


class TaskSearchForm(forms.Form):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    name = forms.CharField(max_length=255, required=False)
    assignees = forms.ModelMultipleChoiceField(queryset=Worker.objects.all(), required=False)
    tasktype = forms.ModelChoiceField(queryset=TaskType.objects.all(), required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)


class UserTaskListSearchForm(forms.Form):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    name = forms.CharField(max_length=255, required=False)
    tasktype = forms.ModelChoiceField(queryset=TaskType.objects.all(), required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)


class ProjectCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = "__all__"
        exclude = ['start_date', 'is_completed']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["team"].queryset = Team.objects.filter(members=user)


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = "__all__"
        exclude = ['start_date', 'is_completed']


class TeamCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Team
        fields = "__all__"
        exclude = ['start_date', 'is_completed']

