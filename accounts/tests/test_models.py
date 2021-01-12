from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            position="Tester",
            email="testuser@email.com"
        )

    def test_username_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_first_name_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_position_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('position').verbose_name
        self.assertEqual(field_label, 'position')

    def test_email_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')

    def test_position_max_length(self):
        user = CustomUser.objects.get(id=1)
        max_length = user._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)

    def test_user_instatiation(self):
        user = CustomUser.objects.get(id=1)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(user.username, "testuser")
        self.assertNotEqual(user.username, "")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertNotEqual(user.email, "")
        self.assertEqual(user.first_name, "Test")
        self.assertNotEqual(user.first_name, "")
        self.assertEqual(user.last_name, "User")
        self.assertNotEqual(user.last_name, "")
        self.assertEqual(user.position, "Tester")
        self.assertNotEqual(user.position, "")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
