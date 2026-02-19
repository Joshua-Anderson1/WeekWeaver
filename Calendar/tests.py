from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# from django.utils.timezone import now
from .models import Calendar


class CalendarModelTest(TestCase):
    """Tests for the calendar model."""

    @classmethod
    def setUpTestData(cls):
        """Create a test user for the author field."""
        newuser = get_user_model()
        user = newuser.objects.create_user(email="testuser@example.com", password="testpass")

        # Create a test Calendar instance
        cls.calendar = Calendar.objects.create(
            author=user,
            calendar_name="Test Calendar",
            notifications="Meeting reminders",
        )

    def test_calendar_name_field(self):
        """Test for seeing if the calendar name works as needed."""
        calendar = self.calendar
        self.assertEqual(calendar.calendar_name, "Test Calendar")

    def test_calendar_notifications_field(self):
        """Test for seeing if the notifications can be added as needed."""
        calendar = self.calendar
        self.assertEqual(calendar.notifications, "Meeting reminders")


class CalendarListViewTests(TestCase):
    """Tests for the calendar list view."""

    @classmethod
    def setUpTestData(cls):
        """Create a Calendar instance for testing."""
        Calendar.objects.create(calendar_name="My Calendar", notifications="Reminders")


class CalendarDetailViewTests(TestCase):
    """Tests for the calendar detail view."""

    @classmethod
    def setUpTestData(cls):
        """Create a Calendar instance."""
        cls.calendar = Calendar.objects.create(
            calendar_name="My Calendar", notifications="Reminders"
        )

    def test_calendar_detail_view_status_code(self):
        """Test that the detail view is accessible."""
        response = self.client.get(reverse("calendar:calendar-detail", args=[self.calendar.id]))
        self.assertEqual(response.status_code, 200)

    def test_calendar_detail_view_template(self):
        """Test that the correct template is used."""
        response = self.client.get(reverse("calendar:calendar-detail", args=[self.calendar.id]))
        self.assertTemplateUsed(response, "Calendar/calendar_detail.html")
