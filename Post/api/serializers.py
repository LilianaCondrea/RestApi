from django.utils.text import slugify
from rest_framework import serializers
from Post.models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='user.username')
    category = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Blog
        fields = [
            'writer', 'content',
            'category', 'description',
            'poster', 'visited', 'created_at',
        ]

    def get_title(self, obj):
        return obj.category.title


class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'content', 'category',
            'description', 'poster'
        ]
        extra_kwargs = {
            'category': {'required': True},
            'poster': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.slug = slugify(instance.content)
        instance.save()
        return instance


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'content', 'description',
            'poster', 'category', 'allow_comment'
        ]
        extra_kwargs = {
            'category': {'required': True},
            'poster': {'required': True},
            'allow_comment': {'required': True},
        }
