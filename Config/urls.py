from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Account.urls')),
    path('blog/', include('Post.urls')),
    path('comment/', include('Comment.urls')),
    # Password Reset
    path('', include('allauth.urls')),

    path('account/api/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('account/api/password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
