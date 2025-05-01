# from django.shortcuts import render

# # Create your views here.
# # tracker/views.py
# from django.views import View
# from django.http import HttpResponse

# class DashboardView(View):
#     def get(self, request):
#         return HttpResponse("Dashboard will go here.")




# # tracker/views.py

# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import ListView, CreateView, UpdateView
# from django.urls import reverse_lazy
# from .models import Task
# from .forms import TaskForm
# from django.contrib.auth.models import Group

# # Dashboard view (temporary)
# from django.http import HttpResponse
# from django.views import View

# class DashboardView(LoginRequiredMixin, View):
#     def get(self, request):
#         return HttpResponse("Dashboard will be updated soon.")


# class TaskListView(LoginRequiredMixin, ListView):
#     model = Task
#     context_object_name = 'tasks'
#     template_name = 'tracker/task_list.html'

#     def get_queryset(self):
#         user = self.request.user
#         if user.groups.filter(name='Manager').exists():
#             return Task.objects.filter(assigned_to__in=[user]) | Task.objects.filter(created_at__isnull=False)
#         return Task.objects.filter(assigned_to=user)


# class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'tracker/task_form.html'
#     success_url = reverse_lazy('task-list')

#     def test_func(self):
#         return self.request.user.groups.filter(name='Manager').exists()

#     def form_valid(self, form):
#         return super().form_valid(form)


# class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'tracker/task_form.html'
#     success_url = reverse_lazy('task-list')

#     def test_func(self):
#         task = self.get_object()
#         return self.request.user == task.assigned_to



# tracker/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import Group
from django.db.models import Count


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            tasks = Task.objects.filter(assigned_to__in=[user]) | Task.objects.filter(created_at__isnull=False)
        else:
            tasks = Task.objects.filter(assigned_to=user)

        # Count by status
        status_summary = tasks.values('status').annotate(count=Count('status'))
        context['tasks'] = tasks
        context['status_summary'] = {item['status']: item['count'] for item in status_summary}
        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tracker/task_list.html'

    def get_queryset(self):
            user = self.request.user
            qs = Task.objects.all() if user.groups.filter(name='Manager').exists() else Task.objects.filter(assigned_to=user)

             # Filter logic
            status = self.request.GET.get('status')
            due = self.request.GET.get('due')

            if status:
                qs = qs.filter(status=status)
            if due:
                qs = qs.filter(due_date=due)

            return qs

            # if user.groups.filter(name='Manager').exists():
            #     return Task.objects.all()  # show all tasks
            # return Task.objects.filter(assigned_to=user)  # show only tasks assigned to the employee



    # def get_queryset(self):
    #     user = self.request.user
    #     if user.groups.filter(name='Manager').exists():
    #         return Task.objects.filter(assigned_to__in=[user]) | Task.objects.filter(created_at__isnull=False)
    #     return Task.objects.filter(assigned_to=user)


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tracker/task_form.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def form_valid(self, form):
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tracker/task_form.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.assigned_to
