from django.urls import reverse_lazy
from django.views import generic

from Calendar.mixins import PaidAuthorRequiredMixin
from Calendar.models import Calendar


# Create your views here.
class CalendarCreateView(generic.CreateView):
    model = Calendar
    fields = ["calendar_name", "events", "notifications"]
    success_url = reverse_lazy("calendar:calendar-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Add Calendar", "button_text": "Add"}

    def form_valid(self, form: object) -> object:
        """For valid form submission.

        - Set the author as the current logged in user.

        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class CalendarListView(generic.ListView):
    model = Calendar
    template_name = "calendar_list.html"
    context_object_name = "calendar"

    # Override get_queryset to filter tasks for the logged-in user
    def get_queryset(self):
        # Filter calendars to only show those where the current user is the author
        return Calendar.objects.filter(author=self.request.user).order_by("-calendar_name")


class CalendarDetailView(generic.DetailView):
    """Detail view of calendar app.

    Default `template_name` if not specified is "calendar/calendar_detail.html"

    """

    model = Calendar


class CalendarUpdateView(AuthorRequiredMixin, generic.UpdateView):
    """View to update calendar."""

    model = Calendar
    fields = ["calendar_name", "events", "notifications"]
    success_url = reverse_lazy("calendar:calendar-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Edit Calendar", "button_text": "Update"}


class CalendarDeleteView(AuthorRequiredMixin, generic.DeleteView):
    """View to delete calendar."""

    model = Calendar
    success_url = reverse_lazy("calendar:calendar-list")
    template_name = "generic_confirm_delete.html"
    extra_context = {"title_text": "Delete Calendar"}
