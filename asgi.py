import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import matching.routing

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blindchinesechess.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blindchinesechess.config.settings.base')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            matching.routing.websocket_urlpatterns
        )
    ),
})
