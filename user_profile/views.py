"""User profile view."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models

FREE, PAID = 1, 2


# Create your views here.
class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """Profile detail view.

    Reason why `slug_field` and `slug_url_kwargs` are set as `None`:
    - By default, in a `DetailView`, the object of the model is retrieved from the URL parameters.
    - In this case, as the model is `UserProfile`, the object of user is retrieved from the request.

    """

    model = models.UserProfile
    template_name = "user_profile/userprofile_detail.html"
    slug_field = None
    slug_url_kwarg = ""

    def get_object(self, queryset: list = None):
        """Owner of the object should be the current user."""
        return self.model.objects.filter(custom_user=self.request.user).first()


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Profile update view."""

    model = models.UserProfile
    form_class = forms.UserProfileUpdateForm
    success_url = reverse_lazy("user_profile:profile_detail")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Update Profile", "button_text": "Update"}

    def get_object(self, queryset: list = None):
        """Get the `UserProfile` object the current logged in user."""
        return self.model.objects.filter(custom_user=self.request.user).first()

    def get_context_data(self, **kwargs):
        """Populate value to the fields in the form."""
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.userprofile

        account_type = 0
        if user_profile.is_free and not user_profile.is_paid:
            account_type = 1
        elif not user_profile.is_free and user_profile.is_paid:
            account_type = 2

        initial = {
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "account_type": account_type,
        }

        context["form"] = forms.UserProfileUpdateForm(instance=user_profile, initial=initial)

        return context

    def form_valid(self, form: object):
        """Set values of the custom_user, is_free, is_paid fields."""
        user_profile = form.save(commit=False)
        user_profile.custom_user = self.request.user

        account_type = 0
        if form.cleaned_data.get("account_type"):
            account_type = int(form.cleaned_data.get("account_type"))

        if not (user_profile.is_free or user_profile.is_paid):
            user_profile.is_free = account_type == FREE
            user_profile.is_paid = account_type == PAID

        custom_user = self.request.user
        custom_user.first_name = form.cleaned_data["first_name"]
        custom_user.last_name = form.cleaned_data["last_name"]
        user_profile.save()
        custom_user.save()

        return super().form_valid(form)
