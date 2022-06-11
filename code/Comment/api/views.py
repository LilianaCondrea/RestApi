from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Response, status
from rest_framework.exceptions import ValidationError
from .serializers import (
    CommentListSerializer, CommentCreateUpdateDeleteSerializer,
    ReplyCommentSerializer
)
from Comment.models import Comments, Reply_Comment
from Post.models import Blog
from Extensions.permissions import IsSuperUserOrOwnerOrReadOnly
from Extensions.throttling import CreateCommentThrottle


class CommentCreateView(CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentCreateUpdateDeleteSerializer
    throttle_classes = [CreateCommentThrottle, ]
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
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        return get_object_or_404(Comments, post=blog, id=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        self.check_object_permissions(request, comment)
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({"message": "comment is deleted !"}, status=status.HTTP_204_NO_CONTENT)


class ReplyCommentListCreateView(APIView):
    serializer_class = ReplyCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_object(self):
        return get_object_or_404(Comments, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.serializer_class(
            Reply_Comment.objects.filter(comment=comment), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if Reply_Comment.objects.filter(comment=comment, user=request.user).exists():
            raise ValidationError('You can only reply once for this comment !')

        if serializer.is_valid(raise_exception=True):
            serializer.save(
                user=request.user,
                comment=comment
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyCommentUpdateDeleteView(APIView):
    serializer_class = ReplyCommentSerializer
    permission_classes = [IsSuperUserOrOwnerOrReadOnly, ]

    def get_object(self):
        return get_object_or_404(Reply_Comment, id=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        reply = self.get_object()
        self.check_object_permissions(request, reply)
        serializer = self.serializer_class(instance=reply, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        reply = self.get_object()
        reply.delete()
        return Response({"message": "reply is deleted !"}, status=status.HTTP_204_NO_CONTENT)
