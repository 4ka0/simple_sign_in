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

        self.assertEqual(testuser.pk, 1)
        self.assertNotEqual(testuser.pk, 2)

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

        self.user = get_user_model().objects.create_user(
            username="johnlennon",
            first_name="John",
            last_name="Lennon",
            email="john@lennon.com",
            password="shikamaru",
            position="songwriter",
        )

        self.client.login(username="johnlennon", password="shikamaru")

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

    def test_complete_registration_form(self):

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

        # Check errors and cleaned data
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

        # Check bound data
        form_output = []

        for boundfield in testuser:
            form_output.append([boundfield.label, boundfield.data])

        expected_output = [
            ["Username", "testuser"],
            ["First name", "Test"],
            ["Last name", "User"],
            ["Position", "Tester"],
            ["Email", "testuser@email.com"],
            ["Password", "testpassword"],
            ["Password confirmation", "testpassword"],
        ]

        self.assertEqual(form_output, expected_output)

    def test_incomplete_registration_form(self):
        """
        If no values are passed to the Form's __init__(), the Form should be
        considered unbound and no validation should be carried out. Form.errors
        should be an empty dictionary but Form.is_valid() should return False.
        """

        # Test empty form
        testuser1 = CustomUserCreationForm()
        self.assertFalse(testuser1.is_bound)
        self.assertEqual(testuser1.errors, {})
        self.assertFalse(testuser1.is_valid())
        with self.assertRaises(AttributeError):
            testuser1.cleaned_data

        # Test partially completed form
        testuser2 = CustomUserCreationForm(
            {
                "username": "testuser",
                "email": "testuser@email.com"
            }
        )
        self.assertEqual(testuser2.errors['first_name'], ['This field is required.'])
        self.assertEqual(testuser2.errors['last_name'], ['This field is required.'])
        self.assertEqual(testuser2.errors['position'], ['This field is required.'])
        self.assertEqual(testuser2.errors['password1'], ['This field is required.'])
        self.assertEqual(testuser2.errors['password2'], ['This field is required.'])
        self.assertFalse(testuser2.is_valid())


class UserUpdatePageTests(TestCase):

    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            position="Tester",
            email="testuser@email.com",
        )

    def test_update_page_by_url(self):
        testuser = get_user_model().objects.get(username="testuser")
        response = self.client.get(f"/accounts/{testuser.pk}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_register_page_by_name(self):
        testuser = get_user_model().objects.get(username="testuser")
        response = self.client.get(reverse("user_update", args=[testuser.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_update_page_uses_correct_template(self):
        testuser = get_user_model().objects.get(username="testuser")
        response = self.client.get(reverse("user_update", args=[testuser.pk]))
        self.assertTemplateUsed(response, "registration/user_update_form.html")
        self.assertTemplateNotUsed(response, "registration/login.html")

    def test_complete_registration_form(self):

        newuser = CustomUserUpdateForm(
            {
                "username": "newuser",
                "email": "newuser@email.com",
                "first_name": "New",
                "last_name": "User",
                "position": "Tester"
            }
        )

        # Check errors and cleaned data
        self.assertTrue(newuser.is_bound)
        self.assertTrue(newuser.is_valid())
        self.assertEqual(newuser.errors, {})
        self.assertEqual(newuser.errors.as_text(), "")

        self.assertEqual(newuser.cleaned_data["username"], "newuser")
        self.assertEqual(newuser.cleaned_data["email"], "newuser@email.com")
        self.assertEqual(newuser.cleaned_data["first_name"], "New")
        self.assertEqual(newuser.cleaned_data["last_name"], "User")
        self.assertEqual(newuser.cleaned_data["position"], "Tester")

        # Check bound data
        form_output = []

        for boundfield in newuser:
            form_output.append([boundfield.label, boundfield.data])

        expected_output = [
            ["Username", "newuser"],
            ["First name", "New"],
            ["Last name", "User"],
            ["Position", "Tester"],
            ["Email", "newuser@email.com"]
        ]

        self.assertEqual(form_output, expected_output)

    def test_incomplete_registration_form(self):

        # Test empty form
        testuser1 = CustomUserCreationForm()
        self.assertFalse(testuser1.is_bound)
        self.assertEqual(testuser1.errors, {})
        self.assertFalse(testuser1.is_valid())
        with self.assertRaises(AttributeError):
            testuser1.cleaned_data

        # Test partially completed form
        testuser2 = CustomUserCreationForm(
            {
                "username": "testuser",
                "email": "testuser@email.com"
            }
        )
        self.assertEqual(testuser2.errors['first_name'], ['This field is required.'])
        self.assertEqual(testuser2.errors['last_name'], ['This field is required.'])
        self.assertEqual(testuser2.errors['position'], ['This field is required.'])
        self.assertEqual(testuser2.errors['password1'], ['This field is required.'])
        self.assertEqual(testuser2.errors['password2'], ['This field is required.'])
        self.assertFalse(testuser2.is_valid())