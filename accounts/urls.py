from django.urls import path

from .views import RegisterView
from .views import CustomUserUpdateView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path( "<int:pk>/update/", CustomUserUpdateView.as_view(), name="user_update"),
]
