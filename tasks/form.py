from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Worker, Position, Task


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
