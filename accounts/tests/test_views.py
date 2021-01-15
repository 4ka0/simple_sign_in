from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class TestRegisterView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')


class TestCustomUserUpdateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            position="Tester",
            email="testuser@email.com"
        )

    def test_view_url_exists_at_desired_location(self):
        testuser = CustomUser.objects.get(id=1)
        response = self.client.get(f'/accounts/{testuser.id}/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        testuser = CustomUser.objects.get(id=1)
        response = self.client.get(reverse('user_update', args=[testuser.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        testuser = CustomUser.objects.get(id=1)
        response = self.client.get(reverse('user_update', args=[testuser.id]))
        self.assertTemplateUsed(response, 'registration/user_update_form.html')


class TestHomePageContent(TestCase):

    def test_home_page_content_when_user_signed_in(self):

        testuser = CustomUser.objects.create(
            username="johnlennon",
            first_name="John",
            last_name="Lennon",
            email="john@lennon.com",
            position="Songwriter"
        )
        testuser.set_password('wibble1234')
        testuser.save()

        login = self.client.login(username="johnlennon", password="wibble1234")
        self.assertTrue(login)

        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "You are logged in as the following user.", 1
        )
        self.assertContains(response, "Username:", 1)
        self.assertContains(response, "johnlennon", 1)
        self.assertContains(response, "Name:", 1)
        self.assertContains(response, "John Lennon", 1)
        self.assertContains(response, "Position:", 1)
        self.assertContains(response, "Songwriter", 1)
        self.assertContains(response, "Email:", 1)
        self.assertContains(response, "john@lennon.com", 1)
        self.assertContains(response, "Date registered:", 1)
        self.assertContains(response, "Last logged in:", 1)
        self.assertNotContains(response, "You are not signed in.")

    def test_home_page_content_when_user_not_signed_in(self):
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