from django.shortcuts import redirect
from django.urls import reverse_lazy

from user_profile.mixins import UserProfileRequiredMixin


class PaidAuthorRequiredMixin(UserProfileRequiredMixin):
    """Paid role and author of the 'Question' object required mixin."""

    def dispatch(self, request, *args, **kwargs):
        """Redirect if the object is not owned by the current user."""
        obj = self.get_object()

        redirect_url = reverse_lazy("Calendar:calendar-list", kwargs={"pk": obj.id})

        if obj.author != self.request.user:
            return redirect(redirect_url)

        return super().dispatch(request, *args, **kwargs)
