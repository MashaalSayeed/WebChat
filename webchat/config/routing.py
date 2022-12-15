from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chat_app.consumer import ChatConsumer


application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                   re_path(r'chat/room/(?P<invite>[A-Z|\d]{8})/$', ChatConsumer)
                ]
            )
        )
    )
})
