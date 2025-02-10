from rest_framework import serializers
from .models import User, Message, GroupChat, Reaction, Notification, Poll, PollOption

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'is_media', 'media_file', 'media_type']

class GroupChatSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True)
    admin = serializers.StringRelatedField()

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'members', 'admin']

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'reaction', 'user', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ['id', 'option_text', 'votes']

class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'creator', 'created_at', 'options']