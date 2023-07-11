from django.urls import path
from gameusers.views import UserCreateView, CheckMatchingView, user_delete_view, delete_matched_users
from gameusers import consumers

urlpatterns = [
    path('addUser/', UserCreateView.as_view(), name='game-match'),
    path('checkMatching/', CheckMatchingView.as_view(), name='check-matching'),
    path('userDelete/', user_delete_view, name='delete_user'),
    path('deleteMatchedUsers/<str:user_id>/', delete_matched_users, name='delete-matched-users'),
]
