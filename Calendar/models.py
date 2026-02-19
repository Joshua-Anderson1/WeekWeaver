from django.db import models


class Calendar(models.Model):
    """Here is the model for Calendar."""

    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    calendar_name = models.CharField(max_length=100)  # Name for Calendar if needed
    events = models.ForeignKey("tasks.Task", on_delete=models.CASCADE, null=True, blank=True)
    notifications = models.CharField(max_length=255)
