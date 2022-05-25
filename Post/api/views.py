from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from Extensions.throttling import CreateBlogThrottle
from Post.models import Blog, Category
from .serializers import (
    BlogListSerializer, BlogCreateSerializer,
    BlogDetailSerializer, CategorySerializer
)
from Extensions.permissions import IsSuperUserOrOwnerOrReadOnly


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ______________________________________________

class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__title', 'allow_comment', ]


# ______________________________________________

class BlogDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUserOrOwnerOrReadOnly, ]
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        return Blog.objects.get(slug__exact=slug)


# ______________________________________________

class BlogCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BlogCreateSerializer
    queryset = Blog.objects.all()
    throttle_classes = [CreateBlogThrottle, ]

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )
