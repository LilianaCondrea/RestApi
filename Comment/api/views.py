from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status
from rest_framework.exceptions import ValidationError
from .serializers import (
    CommentListSerializer, CommentCreateUpdateSerializer, CommentDetailDeleteSerializer
)
from Comment.models import Comments
from Post.models import Blog


class CommentCreateView(CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        blog = Blog.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        if Comments.objects.filter(post=blog, user=user).exists():
            raise ValidationError('You can only comment once for this blog !')
        serializer.save(user=user, post=blog)


class CommentListView(ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comments.objects.all()


class CommentUpdateView(APIView):
    serializer_class = CommentCreateUpdateSerializer

    def get_object(self):
        return get_object_or_404(Comments, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = CommentCreateUpdateSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CommentDetailDeleteView(RetrieveDestroyAPIView):
    serializer_class = CommentDetailDeleteSerializer

    def get_object(self):
        return get_object_or_404(
            Comments,
            id=self.kwargs['pk']
        )
