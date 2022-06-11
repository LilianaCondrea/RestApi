from rest_framework import serializers
from Comment.models import Comments, Reply_Comment


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comments
        fields = (
            'user', 'comment',
            'created_at'
        )


class CommentCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            'comment',
        )


class ReplyCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Reply_Comment
        fields = (
            'user', 'reply_text',
        )
