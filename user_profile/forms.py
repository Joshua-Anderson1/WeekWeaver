"""User Profile Forms."""

from django import forms

from . import models

ACCOUNT_CHOICES = ((1, "Free"), (2, "Paid"))


class UserProfileUpdateForm(forms.ModelForm):
    """User profile change view."""

    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES, required=True)

    class Meta:
        """Meta class."""

        model = models.UserProfile
        fields = [
            "first_name",
            "last_name",
            "gender",
            "age",
            "picture",
            "phone_number",
            "street_address",
            "city",
            "state",
            "about_me",
            "account_type",
        ]
