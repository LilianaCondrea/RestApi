from rest_framework import serializers
from ..models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'content', 'description',
            'poster', 'category',
            'tags'
        ]
        # extra_kwargs = {
        #     'category': {'required': True},
        #     'tags': {'required': True},
        # }
