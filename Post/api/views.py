from rest_framework import generics, permissions
from .serializers import BlogListSerializer, BlogCreateSerializer
from ..models import Blog


class BlogListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = BlogListSerializer

    def get_queryset(self):
        return Blog.objects.all()


class BlogDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = BlogListSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return Blog.objects.get(id=pk)


class BlogCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = BlogCreateSerializer
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )
