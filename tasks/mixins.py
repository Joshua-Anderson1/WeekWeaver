from django.shortcuts import redirect
from django.urls import reverse_lazy

from user_profile.mixins import UserProfileRequiredMixin


class AuthorRequiredMixin(UserProfileRequiredMixin):
    """Free role and author of the 'Task' object required mixin."""

    def dispatch(self, request, *args, **kwargs):
        if not super().test_func():
            return super().handle_no_permission()

        obj = self.get_object()

        redirect_url = reverse_lazy("calendar:calendar-list", kwargs={"pk": obj.id})

        if obj.author != self.request.user:
            return redirect(redirect_url)

        return super().dispatch(request, *args, **kwargs)
