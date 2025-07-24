from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Task


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by task name"}),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
                "style": "width: 300px;",
            }
        ),
    )

    class Meta:
        model = Task
        fields = "__all__"


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )
