from django.urls import path
from .views import CustomUserView, LoginView, ActivateAccountView

urlpatterns = [
  path('login/', LoginView.as_view(), name = "login"),
  path('user/', CustomUserView.as_view(), name = "user"),
  path('activate_user/', ActivateAccountView.as_view(), name = "activate" )
]