from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, SimpleTestCase

from .forms import CustomUserCreationForm, CustomUserUpdateForm


class TestUser(TestCase):
    
    def test_user_creation(self):

        testuser = get_user_model().objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            position="Tester",
            email="testuser@email.com",
        )

        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertNotEqual(get_user_model().objects.all().count(), 0)
        self.assertNotEqual(get_user_model().objects.all().count(), 2)

        self.assertEqual(testuser.username, "testuser")
        self.assertNotEqual(testuser.username, "")

        self.assertEqual(testuser.email, "testuser@email.com")
        self.assertNotEqual(testuser.email, "")

        self.assertEqual(testuser.first_name, "Test")
        self.assertNotEqual(testuser.first_name, "")

        self.assertEqual(testuser.last_name, "User")
        self.assertNotEqual(testuser.last_name, "")

        self.assertEqual(testuser.position, "Tester")
        self.assertNotEqual(testuser.position, "")

        self.assertTrue(testuser.is_active)
        self.assertFalse(testuser.is_staff)
        self.assertFalse(testuser.is_superuser)


class HomePageTests(TestCase):
    def test_home_page_by_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_home_page_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateNotUsed(response, "login.html")

    def test_home_page_display_when_user_signed_in(self):
        # Create user and sign in
        self.user = get_user_model().objects.create_user(
            username="johnlennon",
            first_name="John",
            last_name="Lennon",
            email="john@lennon.com",
            password="shikamaru",
            position="songwriter",
        )
        self.client.login(username="johnlennon", password="shikamaru")
        # Check home page content
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "You are logged in as the following user.", 1
        )
        self.assertContains(response, "Username:", 1)
        self.assertContains(response, "johnlennon", 1)
        self.assertContains(response, "Name:", 1)
        self.assertContains(response, "John Lennon", 1)
        self.assertContains(response, "Position:", 1)
        self.assertContains(response, "songwriter", 1)
        self.assertContains(response, "Email:", 1)
        self.assertContains(response, "john@lennon.com", 1)
        self.assertContains(response, "Date registered:", 1)
        self.assertContains(response, "Last logged in:", 1)
        self.assertNotContains(response, "You are not signed in.")

    def test_home_page_display_when_user_not_signed_in(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "You are not signed in.", 1)
        self.assertNotContains(
            response, "You are logged in as the following user."
        )
        self.assertNotContains(response, "Username:")
        self.assertNotContains(response, "Name:")
        self.assertNotContains(response, "Position:")
        self.assertNotContains(response, "Email:")
        self.assertNotContains(response, "Date registered:")
        self.assertNotContains(response, "Last logged in:")


class RegistrationPageTests(TestCase):
    def test_register_page_by_url(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_register_page_by_name(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_signup_page_uses_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertTemplateNotUsed(response, "registration/login.html")

    def test_registration_form(self):
        # Create new user using custom form
        testuser = CustomUserCreationForm(
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "first_name": "Test",
                "last_name": "User",
                "position": "Tester",
                "password1": "testpassword",
                "password2": "testpassword",
            }
        )
        # Test user creation form
        self.assertTrue(testuser.is_bound)
        self.assertTrue(testuser.is_valid())
        self.assertEqual(testuser.errors, {})
        self.assertEqual(testuser.errors.as_text(), "")
        self.assertEqual(testuser.cleaned_data["username"], "testuser")
        self.assertEqual(testuser.cleaned_data["email"], "testuser@email.com")
        self.assertEqual(testuser.cleaned_data["first_name"], "Test")
        self.assertEqual(testuser.cleaned_data["last_name"], "User")
        self.assertEqual(testuser.cleaned_data["position"], "Tester")
        self.assertEqual(testuser.cleaned_data["password1"], "testpassword")
        self.assertEqual(testuser.cleaned_data["password2"], "testpassword")
