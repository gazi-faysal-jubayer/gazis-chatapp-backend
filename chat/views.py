from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User, Message, GroupChat, Notification, Poll, PollOption, Reaction
from django.db import models
from .serializers import UserSerializer, MessageSerializer, GroupChatSerializer, NotificationSerializer, PollSerializer, ReactionSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

class SendMessageView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class GetMessagesView(APIView):
    def get(self, request, user_id=None, group_id=None):
        if user_id:
            messages = Message.objects.filter(
                (models.Q(sender=request.user, receiver_id=user_id) |
                 models.Q(sender_id=user_id, receiver=request.user))
            ).order_by('timestamp')
        elif group_id:
            messages = Message.objects.filter(group_id=group_id).order_by('timestamp')
        else:
            return Response({'error': 'Invalid request'}, status=400)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class AddFriendView(APIView):
    def post(self, request, friend_id):
        friend = User.objects.get(id=friend_id)
        request.user.friends.add(friend)
        return Response({'status': 'Friend added'})

class SearchUsersView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        users = User.objects.filter(username__icontains=query)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkNotificationAsReadView(APIView):
    def post(self, request, notification_id):
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})

class AddReactionView(APIView):
    def post(self, request, message_id):
        message = Message.objects.get(id=message_id)
        reaction_type = request.data.get('reaction')
        reaction, created = Reaction.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={'reaction': reaction_type}
        )
        if not created:
            reaction.reaction = reaction_type
            reaction.save()
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)

class CreatePollView(APIView):
    def post(self, request):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            poll = serializer.save(creator=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)