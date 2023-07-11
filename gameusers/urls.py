from django.urls import path
from matching import consumers

urlpatterns = [
    path('establishSession/', consumers.MatchConsumer.as_asgi()),
]
