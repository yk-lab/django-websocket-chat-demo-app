from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from ..models import Room


class RoomView(LoginRequiredMixin, DetailView):
    queryset = Room.objects\
        .prefetch_related('messages')
    template_name = 'chat/chat_room.html'


room_view = RoomView.as_view()
