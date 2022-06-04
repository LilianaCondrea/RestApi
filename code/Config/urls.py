from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Blog Writen With Drf",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aqaarsham@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Account.urls')),
    path('blog/', include('Post.urls')),
    path('comment/', include('Comment.urls')),

    # Password Reset
    path('account/api/password_reset/',
         PasswordResetView.as_view(), name='password_reset'),
    path('account/api/password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Verification Email
    path('account/api/resend_verification_email/',
         ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('account/api/email_verification_sent/',
         ConfirmEmailView.as_view(), name='account_email_verification_sent'),
    path('account/api/confirm-email/<str:key>/',
         VerifyEmailView.as_view(), name='account_confirm_email'),

    # Api Documentation
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
