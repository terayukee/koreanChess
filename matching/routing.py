# routing.py
from django.urls import re_path
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/establishSession/(?P<userId>\w+)', consumers.MyConsumer.as_asgi()),
    path('ws/establishSession/<str:userId>', consumers.MatchConsumer.as_asgi()),
]
