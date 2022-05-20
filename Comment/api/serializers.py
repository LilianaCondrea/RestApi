from rest_framework import serializers
from Comment.models import Comments


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.content')

    class Meta:
        model = Comments
        fields = (
            'user', 'post', 'comment'
        )


class CommentDetailDeleteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.content')

    class Meta:
        model = Comments
        fields = '__all__'


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            'comment',
        )
