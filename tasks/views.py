from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

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
    paginate_by = 5
    queryset = Task.objects.all()

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(TasksListView, self).get_context_data(**kwargs)
        context["todo_tasks"] = Task.objects.filter(status="todo")
        context["in_progress_tasks"] = Task.objects.filter(status="in_progress")
        context["done_tasks"] = Task.objects.filter(status="done")
        context["needs_review_tasks"] = Task.objects.filter(status="needs_review")
    #     name = self.request.GET.get("name", "")
    #     context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    # def get_queryset(self):
    #     name = self.request.GET.get("name", "")
    #     if name:
    #         return self.queryset.filter(name__icontains=name)
    #     return self.queryset