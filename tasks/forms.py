from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from tasks.models import Task, Worker


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by task name",
            "class": "search-input",
        }),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Assignees",
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control item",
                "placeholder": "Deadline",
            }
        ),
    )

    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees", "status")
        labels = {
            "status": "Select Task Status",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control item", "placeholder": "Task Name"}),
            "description": forms.Textarea(attrs={"class": "form-control item", "placeholder": "Description"}),
            "priority": forms.Select(attrs={"class": "form-control item"}),
            "task_type": forms.Select(attrs={"class": "form-control item"}),
            "status": forms.Select(attrs={"class": "form-control item"}),
        }


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by username",
            "class": "search-input",
        }),
    )


class WorkerCreateForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )
