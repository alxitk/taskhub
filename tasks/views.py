from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskSearchForm, TaskForm, WorkerSearchForm, WorkerCreateForm
from tasks.models import Worker, Task


def index(request):
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "tasks/index.html", context=context)


class TasksListView(generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    queryset = Task.objects.all()

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        if name:
            return self.queryset.filter(name__icontains=name)
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_queryset = self.get_queryset()

        context["todo_tasks"] = filtered_queryset.filter(status="todo")
        context["in_progress_tasks"] = filtered_queryset.filter(status="in_progress")
        context["done_tasks"] = filtered_queryset.filter(status="done")
        context["needs_review_tasks"] = filtered_queryset.filter(status="needs_review")

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:tasks-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:tasks-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:tasks-list")


class WorkerListView(generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "tasks/worker_list.html"

    def get_queryset(self):
        queryset = Worker.objects.all()
        username = self.request.GET.get("username", "")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username})
        return context


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDetailView(generic.DetailView):
    queryset = Worker.objects.all().prefetch_related("tasks__assignees")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name" ,"position",)
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


def toggle_assign_to_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    user = request.user
    if user in task.assignees.all():
        task.assignees.remove(user)
    else:
        task.assignees.add(user)
    return HttpResponseRedirect(reverse_lazy("tasks:task-detail", args=[pk]))


