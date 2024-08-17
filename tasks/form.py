from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django.utils import timezone

from tasks.models import Worker, Position, Task, TaskType, Project, Team


class WorkerCreateForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label=None,
        required=False,
    )

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


class WorkerSearchForm(forms.Form):
    username = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)


class TaskSearchForm(forms.Form):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    ]
    name = forms.CharField(max_length=255, required=False)
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        required=False
    )
    tasktype = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)


class DeadlineValidationMixin:
    """A mixin to validate deadlines for form or model data.
    """

    def clean_deadline(self):
        """Validate that the deadline is not set to a time in the past."""

        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise ValidationError("The deadline cannot be in the past.")
        return deadline

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get('deadline')
        is_completed = cleaned_data.get('is_completed')

        if is_completed and deadline and deadline < timezone.now():
            self.add_error(
                "deadline",
                "The deadline cannot be in the past when marked as completed."
            )
        return cleaned_data


class UserTaskListSearchForm(forms.Form):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    ]
    name = forms.CharField(max_length=255, required=False)
    tasktype = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)


class ProjectCreateForm(DeadlineValidationMixin, forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = "__all__"
        exclude = ["start_date", "is_completed"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["teams"].queryset = Team.objects.filter(members=user)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Project'))
        self.fields['deadline'].widget = (
            forms.DateInput(attrs={'type': 'date'})
        )


class TaskCreateForm(DeadlineValidationMixin, forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )

    class Meta:
        model = Task
        fields = "__all__"
        exclude = ["start_date", "is_completed"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Task'))
        self.fields['deadline'].widget = (
            forms.DateInput(attrs={'type': 'date'})
        )


class TeamCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )

    class Meta:
        model = Team
        fields = "__all__"
        exclude = ["start_date", "is_completed", "created_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Team'))
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['members'].widget.attrs.update({'class': 'form-control'})


class TeamSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Name")
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Start Date"
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Name")
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Start Date"
    )
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Deadline"
    )
