from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView

from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomUserUpdateForm,
)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy("home")
    template_name = "registration/user_update_form.html"
