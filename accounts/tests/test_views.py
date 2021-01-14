from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class TestRegisterView(SimpleTestCase):
    """
    class RegisterView(CreateView):
        form_class = CustomUserCreationForm
        success_url = reverse_lazy("login")
        template_name = "registration/register.html"
    """

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
    """
    class CustomUserUpdateView(UpdateView):
        model = CustomUser
        form_class = CustomUserUpdateForm
        success_url = reverse_lazy("home")
        template_name = "registration/user_update_form.html"
    """

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
