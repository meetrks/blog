from django.contrib.auth.models import User
from rest_framework import serializers

from log.models import Blog, Topic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'first_name', 'last_name', 'email'


class TopicSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = Topic
        exclude = 'created', 'modified',

    def create(self, validated_data):
        instance = Topic.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.topic = validated_data.get('topic', instance.topic)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


class BlogSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    slug = serializers.SlugField(write_only=True)
    related_topics = TopicSerializer(many=True, read_only=True)
    shared_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        exclude = 'created', 'modified',

    @staticmethod
    def get_shared_link(obj):
        return '/blog/{}/{}/'.format(obj.pk, obj.slug)

    @staticmethod
    def validate_topic(topics):
        try:
            return [Topic.objects.get(pk=t['id']) for t in topics]
        except:
            raise serializers.ValidationError({"detail": "Invalid topic selected"})

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Blog.objects.create(creator=user, **validated_data)
        instance.related_topics.add(*self.validate_topic(self.context['request'].data.get('related_topics', None)))
        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.related_topics.clear()
        instance.related_topics.add(*self.validate_topic(self.context['request'].data.get('related_topics', None)))
        instance.save()
        return instance
