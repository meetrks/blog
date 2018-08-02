from rest_framework import serializers

from admin_app.models import Comment
from admin_app.serializers import UserSerializer


class RecursiveReplySerializer(serializers.Serializer):
    def to_representation(self, sample):
        serializer = self.parent.parent.__class__(sample, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer(read_only=True)
    reply = RecursiveReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        exclude = 'created', 'modified', 'parent'

    def create(self, validated_data):
        user = self.context['request'].user
        parent_comment = self.context['request'].data.get('parent', None)
        instance = Comment.objects.create(commented_by=user, **validated_data)
        if parent_comment:
            instance.parent = Comment.objects.get(pk=parent_comment)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
