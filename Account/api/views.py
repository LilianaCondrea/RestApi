from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import Profile
from .serializers import (
    UserListSerializer, UserDetailSerializer, ProfileUserSerializer
)
from .permissions import IsSuperUserOrOwner, IsSuperUser


class UserListView(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = UserListSerializer

    def get_queryset(self):
        return get_user_model().objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUserOrOwner,)
    serializer_class = UserDetailSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(get_user_model(), id=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class ProfileUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUserOrOwner,)
    serializer_class = ProfileUserSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(Profile, user_id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
