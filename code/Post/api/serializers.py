from django.utils.text import slugify
from rest_framework import serializers
from Post.models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='blog_detail',
        lookup_field='slug'
    )
    writer = serializers.ReadOnlyField(source='user.username')
    category = serializers.SerializerMethodField('get_title')
    description = serializers.SerializerMethodField('get_description')

    class Meta:
        model = Blog
        fields = [
            'url', 'writer', 'content',
            'category', 'poster',
            'description', 'published_at',
        ]

    def get_title(self, obj):
        return obj.category.title

    def get_description(self, obj):
        return obj.description[:150] + '...'


class BlogDetailSerializer(serializers.ModelSerializer):
    share = serializers.HyperlinkedIdentityField(
        view_name='Post:blog_detail',
        lookup_field='slug',
    )
    likes = serializers.SerializerMethodField()
    writer = serializers.ReadOnlyField(source='user.username')
    category = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'share', 'writer', 'content',
            'category', 'description', 'poster',
            'likes', 'visited', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['likes']
        extra_kwargs = {
            'poster': {'required': True},
        }

    def get_likes(self, obj):
        return {
            'count': obj.likes.count(),
            'user': [user.username for user in obj.likes.all()]
        }

    def get_category(self, obj):
        return obj.category.title

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
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
