from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    # Overidden to be required fields
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'username',
            'first_name',
            'last_name',
            'position',
            'email',
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Used for the user to change his/her password.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'position', 'email',)


class CustomUserUpdateForm(ModelForm):
    """
    Used for the user to change his/her user details apart from the password.
    """

    # Overidden to be required fields
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'position', 'email',)