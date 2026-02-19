from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser  # Assuming CustomUser is in the 'users' app

from .models import UserProfile


# Create your tests here.
class UserProfileModelTest(TestCase):
    """Test the UserProfile model."""

    def setUp(self):
        """Set up test data."""
        self.custom_user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_user_profile_created_on_user_creation(self):
        """Test that a UserProfile is created automatically when a CustomUser is created."""
        # Ensure UserProfile was created
        user_profile = UserProfile.objects.get(custom_user=self.custom_user)
        self.assertEqual(user_profile.custom_user, self.custom_user)

    def test_default_gender_is_none(self):
        """Test that the default gender is 'NONE' (0)."""
        user_profile = UserProfile.objects.get(custom_user=self.custom_user)
        self.assertEqual(user_profile.gender, UserProfile.Gender.NONE)

    def test_default_age_is_21(self):
        """Test that the default age is 21."""
        user_profile = UserProfile.objects.get(custom_user=self.custom_user)
        self.assertEqual(user_profile.age, 21)

    def test_default_is_paid_is_false(self):
        """Test that the default 'is_paid' value is False."""
        user_profile = UserProfile.objects.get(custom_user=self.custom_user)
        self.assertFalse(user_profile.is_paid)

    def test_default_is_free_is_false(self):
        """Test that the default 'is_free' value is False."""
        user_profile = UserProfile.objects.get(custom_user=self.custom_user)
        self.assertFalse(user_profile.is_free)

    def test_default_phone_number_is_10(self):
        """Test that the default phone_number is 10."""
        user_profile = UserProfile.objects.get(custom_user=self.custom_user)
        self.assertEqual(user_profile.phone_number, 10)

    def test_create_profile_signal(self):
        """Test that the post_save signal creates a UserProfile when a CustomUser is created."""
        new_user = CustomUser.objects.create_user(
            email="newuser@example.com", password="newpassword"
        )
        # Check if the profile is created
        self.assertTrue(UserProfile.objects.filter(custom_user=new_user).exists())


class UserProfileViewTests(TestCase):
    """Test the UserProfile views."""

    def setUp(self):
        """Set up test data."""
        # Create a CustomUser instance using 'email' as the identifier
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",  # Use 'email' instead of 'username'
            password="testpassword",
        )

        # Ensure that the UserProfile is created only once for this user
        self.user_profile, created = UserProfile.objects.get_or_create(
            custom_user=self.user,
            defaults={
                "street_address": "123 Main St",
                "city": "Test City",
                "state": "Test State",
                "about_me": "This is a test user.",
            },
        )

        # URLs for the views
        self.profile_url = reverse(
            "user_profile:profile_detail"
        )  # Assuming the URL name is 'profile_detail'
        self.profile_update_url = reverse(
            "user_profile:profile_update"
        )  # Assuming the URL name is 'profile_update'

    def test_user_profile_detail_view(self):
        """Test that the profile detail page is only accessible by the logged-in user."""
        # Test the view when logged in
        self.client.login(email="testuser@example.com", password="testpassword")  # Login with email
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/userprofile_detail.html")

        # Test the view when not logged in (should redirect)
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.profile_url}")

    def test_user_profile_update_view_get(self):
        """Test that the profile update page is only accessible by the logged-in user."""
        # Test the view when logged in
        self.client.login(email="testuser@example.com", password="testpassword")  # Login with email
        response = self.client.get(self.profile_update_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update Profile")
        self.assertTemplateUsed(response, "generic_create_update_form.html")

        # Check if form is pre-populated with the user's current data
        self.assertEqual(response.context["form"].initial["first_name"], self.user.first_name)
        self.assertEqual(response.context["form"].initial["last_name"], self.user.last_name)

        # Test the view when not logged in (should redirect)
        self.client.logout()
        response = self.client.get(self.profile_update_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.profile_update_url}")
