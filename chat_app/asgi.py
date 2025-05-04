import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# Ensure Django is fully loaded before importing anything that uses models/settings
django.setup()

# Now safe to import routing
from chat import routing

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
    ),
})
