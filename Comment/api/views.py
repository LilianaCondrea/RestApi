from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status
from rest_framework.exceptions import ValidationError
from .serializers import (
    CommentListSerializer, CommentCreateUpdateDeleteSerializer
)
from Comment.models import Comments
from Post.models import Blog
from permissions import IsSuperUserOrOwnerOrReadOnly


class CommentCreateView(CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentCreateUpdateDeleteSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        blog = get_object_or_404(Blog, id=self.kwargs['pk'])
        user = self.request.user
        if Comments.objects.filter(post=blog, user=user).exists():
            raise ValidationError('You can only comment once for this blog !')
        elif blog.allow_comment is False:
            raise ValidationError('This blog is not open for commenting !')
        serializer.save(user=user, post=blog)


# __________________________________________________________________-

class CommentListView(APIView):
    serializer_class = CommentListSerializer

    def get_object(self):
        blog = get_object_or_404(Blog, id=self.kwargs['pk'])
        return Comments.objects.filter(post=blog)

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# _____________________- __________________________________________________

class CommentUpdateDeleteView(APIView):
    serializer_class = CommentCreateUpdateDeleteSerializer
    permission_classes = [IsSuperUserOrOwnerOrReadOnly, ]

    def get_object(self):
        blog = get_object_or_404(Blog, id=self.kwargs['pk'])
        return get_object_or_404(Comments, post=blog, user=self.request.user)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response({"message": "comment is deleted !"}, status=status.HTTP_204_NO_CONTENT)
