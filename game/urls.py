from django.urls import path
from . import views
from . import match

urlpatterns = [
    path('getGameInfo/', views.GameInfoView.as_view(), name='get_game_info'),
    path('establishSession/<str:match_id>/', views.establish_session, name='establish_session'),
]
