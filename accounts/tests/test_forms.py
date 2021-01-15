from django.test import TestCase, SimpleTestCase

from accounts.forms import CustomUserCreationForm, CustomUserUpdateForm


class CustomUserCreationFormTests(TestCase):
    def test_custom_user_creation_form_field_labels(self):
        form = CustomUserCreationForm()
        self.assertTrue(
            form.fields["username"].label == "Username"
            or form.fields["username"].label == None
        )
        self.assertTrue(
            form.fields["first_name"].label == "First name"
            or form.fields["first_name"].label == None
        )
        self.assertTrue(
            form.fields["last_name"].label == "Last name"
            or form.fields["last_name"].label == None
        )
        self.assertTrue(
            form.fields["position"].label == "Position"
            or form.fields["position"].label == None
        )
        self.assertTrue(
            form.fields["email"].label == "Email"
            or form.fields["email"].label == None
        )

    def test_custom_user_creation_form_required_fields(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields["username"].required)
        self.assertTrue(form.fields["first_name"].required)
        self.assertTrue(form.fields["last_name"].required)
        self.assertTrue(form.fields["position"].required)
        self.assertTrue(form.fields["email"].required)

    def test_custom_user_creation_form_field_maxlengths(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields["first_name"].max_length == 150)
        self.assertTrue(form.fields["last_name"].max_length == 150)

    def test_custom_user_creation_form_when_valid(self):
        form = CustomUserCreationForm(
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

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertEqual(form.errors.as_text(), "")

        self.assertEqual(form.cleaned_data["username"], "testuser")
        self.assertEqual(form.cleaned_data["email"], "testuser@email.com")
        self.assertEqual(form.cleaned_data["first_name"], "Test")
        self.assertEqual(form.cleaned_data["last_name"], "User")
        self.assertEqual(form.cleaned_data["position"], "Tester")
        self.assertEqual(form.cleaned_data["password1"], "testpassword")
        self.assertEqual(form.cleaned_data["password2"], "testpassword")

        # Check bound data
        form_output = []

        for boundfield in form:
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

    def test_custom_user_creation_form_when_empty(self):
        form = CustomUserCreationForm()
        self.assertFalse(form.is_bound)
        self.assertEqual(
            form.errors, {}
        )  # Should be an empty dictionary as validation is not carried out.
        self.assertFalse(form.is_valid())
        with self.assertRaises(AttributeError):
            form.cleaned_data

    def test_custom_user_creation_form_when_partially_empty(self):
        form = CustomUserCreationForm(
            {"username": "testuser", "email": "testuser@email.com"}
        )
        self.assertEqual(
            form.errors["first_name"], ["This field is required."]
        )
        self.assertEqual(form.errors["last_name"], ["This field is required."])
        self.assertEqual(form.errors["position"], ["This field is required."])
        self.assertEqual(form.errors["password1"], ["This field is required."])
        self.assertEqual(form.errors["password2"], ["This field is required."])
        self.assertFalse(form.is_valid())


class CustomUserUpdateFormTests(TestCase):
    def test_custom_user_update_form_field_labels(self):
        form = CustomUserUpdateForm()
        self.assertTrue(
            form.fields["username"].label == "Username"
            or form.fields["username"].label == None
        )
        self.assertTrue(
            form.fields["first_name"].label == "First name"
            or form.fields["first_name"].label == None
        )
        self.assertTrue(
            form.fields["last_name"].label == "Last name"
            or form.fields["last_name"].label == None
        )
        self.assertTrue(
            form.fields["position"].label == "Position"
            or form.fields["position"].label == None
        )
        self.assertTrue(
            form.fields["email"].label == "Email"
            or form.fields["email"].label == None
        )

    def test_custom_user_update_form_required_fields(self):
        form = CustomUserUpdateForm()
        self.assertTrue(form.fields["username"].required)
        self.assertTrue(form.fields["first_name"].required)
        self.assertTrue(form.fields["last_name"].required)
        self.assertTrue(form.fields["position"].required)
        self.assertTrue(form.fields["email"].required)

    def test_custom_user_update_form_field_maxlengths(self):
        form = CustomUserUpdateForm()
        self.assertTrue(form.fields["first_name"].max_length == 150)
        self.assertTrue(form.fields["last_name"].max_length == 150)

    def test_custom_user_update_form_when_valid(self):
        form = CustomUserUpdateForm(
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "first_name": "Test",
                "last_name": "User",
                "position": "Tester",
            }
        )

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertEqual(form.errors.as_text(), "")

        self.assertEqual(form.cleaned_data["username"], "testuser")
        self.assertEqual(form.cleaned_data["email"], "testuser@email.com")
        self.assertEqual(form.cleaned_data["first_name"], "Test")
        self.assertEqual(form.cleaned_data["last_name"], "User")
        self.assertEqual(form.cleaned_data["position"], "Tester")

        # Check bound data
        form_output = []

        for boundfield in form:
            form_output.append([boundfield.label, boundfield.data])

        expected_output = [
            ["Username", "testuser"],
            ["First name", "Test"],
            ["Last name", "User"],
            ["Position", "Tester"],
            ["Email", "testuser@email.com"],
        ]

        self.assertEqual(form_output, expected_output)

    def test_custom_user_update_form_when_empty(self):
        form = CustomUserUpdateForm()
        self.assertFalse(form.is_bound)
        self.assertEqual(
            form.errors, {}
        )  # Should be an empty dictionary as validation is not carried out.
        self.assertFalse(form.is_valid())
        with self.assertRaises(AttributeError):
            form.cleaned_data

    def test_custom_user_update_form_when_partially_empty(self):
        form = CustomUserUpdateForm(
            {"username": "testuser", "email": "testuser@email.com"}
        )
        self.assertEqual(
            form.errors["first_name"], ["This field is required."]
        )
        self.assertEqual(form.errors["last_name"], ["This field is required."])
        self.assertEqual(form.errors["position"], ["This field is required."])
        self.assertFalse(form.is_valid())
