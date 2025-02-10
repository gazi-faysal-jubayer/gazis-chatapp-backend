from django.urls import path
from .views import (
    SignupView, LoginView, SendMessageView, GetMessagesView,
    AddFriendView, SearchUsersView, NotificationListView,
    MarkNotificationAsReadView, AddReactionView, CreatePollView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('get-messages/<int:user_id>/', GetMessagesView.as_view(), name='get-messages-user'),
    path('get-messages/group/<int:group_id>/', GetMessagesView.as_view(), name='get-messages-group'),
    path('add-friend/<int:friend_id>/', AddFriendView.as_view(), name='add-friend'),
    path('search-users/', SearchUsersView.as_view(), name='search-users'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('mark-notification-read/<int:notification_id>/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('add-reaction/<int:message_id>/', AddReactionView.as_view(), name='add-reaction'),
    path('create-poll/', CreatePollView.as_view(), name='create-poll'),
]