from django.db import models


class Task(models.Model):
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=200)
    task_deadline = models.DateTimeField("due date", help_text="Must be in YYYY-MM-DD format")
    recurring = models.BooleanField(default=False)
    preparation = models.BooleanField(default=False)
    how_much_prep = models.CharField(max_length=200)

    def __str__(self):
        return self.task_name  # This will display the task_name in related fields

    class PriorityLevel(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"

    priority_level = models.CharField(max_length=6, choices=PriorityLevel.choices, default="Low")
