# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.DashboardView.as_view(), name='dashboard'),
#     # We will add more routes later (task list, create, update)
# ]


# tracker/urls.py

from django.urls import path
from .views import DashboardView, TaskListView, TaskCreateView, TaskUpdateView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
]
