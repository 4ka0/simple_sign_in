from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, SimpleTestCase


class HomePageTests(TestCase):

    def test_home_page_by_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_home_page_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateNotUsed(response, 'login.html')

    # up to here

    def test_home_page_display_when_user_signed_in(self):

        # this login section does not work
        testuser = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            first_name='Test',
            last_name='User',
            position='Tester',
            password='shikamaru'
        )
        self.client.force_login(testuser)

        response = self.client.get(reverse('home'))
        self.assertContains(response, "You are logged in as the following user.", 1)
        self.assertContains(response, "Username:", 1)
        self.assertContains(response, "Position:", 1)
        self.assertContains(response, "Email:", 1)
        self.assertContains(response, "Date registered:", 1)
        self.assertContains(response, "Last logged in:", 1)


    def test_home_page_display_when_user_signed_out(self):
        pass



class RegisterPageTests(TestCase):

    def test_register_page_by_url(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_register_page_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)

    def test_signup_page_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertTemplateNotUsed(response, 'registration/login.html')

    def test_registration_form(self):

        testuser = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            first_name='Test',
            last_name='User',
            position='Tester'
        )

        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertNotEqual(get_user_model().objects.all().count(), 2)

        self.assertEqual(testuser.username, 'testuser')
        self.assertNotEqual(testuser.username, '')

        self.assertEqual(testuser.email, 'testuser@email.com')
        self.assertNotEqual(testuser.email, '')

        self.assertEqual(testuser.first_name, 'Test')
        self.assertNotEqual(testuser.first_name, '')

        self.assertEqual(testuser.last_name, 'User')
        self.assertNotEqual(testuser.last_name, '')

        self.assertEqual(testuser.position, 'Tester')
        self.assertNotEqual(testuser.position, '')

        self.assertTrue(testuser.is_active)
        self.assertFalse(testuser.is_staff)
        self.assertFalse(testuser.is_superuser)