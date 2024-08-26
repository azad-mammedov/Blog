from django.urls import path

from custom_auth.views import (
    LoginView ,
    RegisterView,
    ChangePasswordView,
    LogoutView
)

urlpatterns = [
    path('login',LoginView.as_view(), name='login'),
    path('register',RegisterView.as_view(), name='register'),
    path('change-password',ChangePasswordView.as_view(), name='change-password'),
    path('logout',LogoutView.as_view(),name='logout')
]
