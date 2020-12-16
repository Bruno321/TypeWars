# django
from django.urls import re_path

# local
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/game/test/(?P<room_name>\w+)/$',consumers.ChatConsumer.as_asgi()),
]
# print(websocket_urlpatterns)
# localhost:800/game/test/asd
# localhost:8000/game/test/<asd>  /ws/chat/<asd>/
# ws/chat/<asd>/
