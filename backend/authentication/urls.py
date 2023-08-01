from django.urls import path
from .views import CustomUserView, LoginView

urlpatterns = [
  path('login/', LoginView.as_view(), name = "login"),
  path('user/', CustomUserView.as_view(), name = "user"),
]