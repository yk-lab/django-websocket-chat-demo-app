from django.urls import path
from rest_framework_nested import routers

from .views import index_view, room_view
from .viewsets import RoomViewset

app_name = 'chat'

router = routers.SimpleRouter()
router.register('rooms', RoomViewset)

urlpatterns = [
    path('', index_view, name='index'),
    path('room/<str:pk>', room_view, name='room'),
] + router.urls
