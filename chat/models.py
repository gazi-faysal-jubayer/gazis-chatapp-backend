from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)

    class Meta:
        # Add related_name to avoid clashes with auth.User
        swappable = 'AUTH_USER_MODEL'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Override groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='chat_users',  # Add a unique related_name
        related_query_name='chat_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='chat_users',  # Add a unique related_name
        related_query_name='chat_user',
    )

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey('GroupChat', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_media = models.BooleanField(default=False)
    media_file = models.FileField(upload_to='media/', blank=True, null=True)
    media_type = models.CharField(max_length=50, blank=True, null=True)

class GroupChat(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='group_chats')
    admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]

    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reactions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Poll(models.Model):
    question = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='polls', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    vote_count = models.IntegerField(default=0)  # Rename "votes" to "vote_count"

class PollVote(models.Model):
    poll_option = models.ForeignKey(
        PollOption,
        related_name='votes',  # Add a unique related_name
        on_delete=models.CASCADE
    )
    voter = models.ForeignKey(User, related_name='poll_votes', on_delete=models.CASCADE)