from django.urls import path, include

urlpatterns = [
    path('api/', include('Comment.api.urls')),
]
