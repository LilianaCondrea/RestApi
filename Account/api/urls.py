from django.urls import path
from dj_rest_auth import views
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import UserListView, UserDetailView, ProfileUserView

app_name = "Account"

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='rest_login'),
    path('logout/', views.LogoutView.as_view(), name='rest_logout'),

    path('register/', RegisterView.as_view(), name='rest_register'),
    path('verify_email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    path('password/change/', views.PasswordChangeView.as_view(), name='rest_password_change'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/profile/<int:pk>/', ProfileUserView.as_view(), name='user_profile'),

]
