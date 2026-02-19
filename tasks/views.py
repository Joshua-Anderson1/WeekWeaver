from django.urls import reverse_lazy
from django.views import generic

from tasks.mixins import AuthorRequiredMixin
from tasks.models import Task


class CreateTaskView(generic.CreateView):
    """View to create task."""

    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Add Task", "button_text": "Add"}

    fields = []

    def get_fields_based_on_profile(self):
        """Return the list of fields based on user profile."""
        if self.request.user.is_authenticated:
            if self.request.user.userprofile.is_free:
                # If the user is free, only show 'recurring' field
                return [
                    "task_name",
                    "task_deadline",
                    "recurring",
                    "priority_level",
                ]
            elif self.request.user.userprofile.is_paid:
                # If the user is paid, show all fields
                return [
                    "task_name",
                    "task_deadline",
                    "recurring",
                    "preparation",
                    "how_much_prep",
                    "priority_level",
                ]
            else:
                return [
                    "task_name",
                    "task_deadline",
                    "priority_level",
                ]

        return [
            "task_name",
            "task_deadline",
            "priority_level",
        ]

    def get_form_class(self):
        """Override to modify the form class dynamically."""
        # Get the default form class
        form_class = super().get_form_class()

        # Dynamically update the form fields based on the user's profile
        self.fields = self.get_fields_based_on_profile()

        # Return the form class with the updated fields
        class DynamicTaskForm(form_class):
            class Meta:
                model = Task
                fields = self.fields  # Use the updated fields dynamically

        return DynamicTaskForm

    def get_form(self, *args, **kwargs):
        """Override to adjust fields based on user profile."""
        form = super().get_form(*args, **kwargs)
        # Dynamically set the fields based on the user's profile
        form.fields = {field: form.fields[field] for field in self.get_fields_based_on_profile()}
        return form

    def form_valid(self, form: object) -> object:
        """For valid form submission.

        - Set the author as the current logged in user.

        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskListView(generic.ListView):
    """Task list view."""

    model = Task
    queryset = Task.objects.order_by("-task_deadline")[:5]
    template_name = "task_list.html"
    context_object_name = "tasks"

    # Override get_queryset to filter tasks for the logged-in user
    def get_queryset(self):
        # Filter tasks to only show those where the current user is the author
        return Task.objects.filter(author=self.request.user).order_by("-task_deadline")


class TaskDetailView(AuthorRequiredMixin, generic.DetailView):
    """Detail view of individual tasks."""

    model = Task
    template_name = "tasks/task_details.html"
    context_object_name = "tasks"


class UpdateTaskView(AuthorRequiredMixin, generic.UpdateView):
    """View to update task."""

    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Add Task", "button_text": "Add"}

    fields = []

    def get_fields_based_on_profile(self):
        """Return the list of fields based on user profile."""
        if self.request.user.is_authenticated:
            if self.request.user.userprofile.is_free:
                # If the user is free, only show 'recurring' field
                return [
                    "task_name",
                    "task_deadline",
                    "recurring",
                    "priority_level",
                ]
            elif self.request.user.userprofile.is_paid:
                # If the user is paid, show all fields
                return [
                    "task_name",
                    "task_deadline",
                    "recurring",
                    "preparation",
                    "how_much_prep",
                    "priority_level",
                ]
            else:
                return [
                    "task_name",
                    "task_deadline",
                    "priority_level",
                ]

        return [
            "task_name",
            "task_deadline",
            "priority_level",
        ]

    def get_form_class(self):
        """Override to modify the form class dynamically."""
        # Get the default form class
        form_class = super().get_form_class()

        # Dynamically update the form fields based on the user's profile
        self.fields = self.get_fields_based_on_profile()

        # Return the form class with the updated fields
        class DynamicTaskForm(form_class):
            class Meta:
                model = Task
                fields = self.fields  # Use the updated fields dynamically

        return DynamicTaskForm

    def get_form(self, *args, **kwargs):
        """Override to adjust fields based on user profile."""
        form = super().get_form(*args, **kwargs)
        # Dynamically set the fields based on the user's profile
        form.fields = {field: form.fields[field] for field in self.get_fields_based_on_profile()}
        return form

    def form_valid(self, form: object) -> object:
        """For valid form submission.

        - Set the author as the current logged in user.

        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteTaskView(AuthorRequiredMixin, generic.DeleteView):
    """View to delete task."""

    model = Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "generic_confirm_delete.html"
    extra_context = {"title_text": "Delete Task"}
