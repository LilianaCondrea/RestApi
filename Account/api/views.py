from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from ..models import Profile
from .serializers import (
    UserListSerializer, UserDetailSerializer, ProfileUserSerializer
)
from Extensions.permissions import IsSuperUserOrUserOrReadOnly, IsSuperUser
from Extensions.pagination import CustomPagination


class UserListView(ListAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = UserListSerializer
    filterset_fields = ('username', 'is_superuser')
    search_fields = ['email', 'phone']
    ordering_fields = ['date_joined', 'is_superuser']
    pagination_class = CustomPagination

    def get_queryset(self):
        return get_user_model().objects.all()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUserOrUserOrReadOnly,)
    serializer_class = UserDetailSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(get_user_model(), id=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class ProfileUserView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUserOrUserOrReadOnly,)
    serializer_class = ProfileUserSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(Profile, user_id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
