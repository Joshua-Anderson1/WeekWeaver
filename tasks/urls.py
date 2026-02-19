from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    path("tasks/add/", views.CreateTaskView.as_view(), name="create-task"),
    path("tasks", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-details"),
    path("tasks/<int:pk>/edit", views.UpdateTaskView.as_view(), name="update-task"),
    path("tasks/<int:pk>/delete", views.DeleteTaskView.as_view(), name="delete-task"),
]
