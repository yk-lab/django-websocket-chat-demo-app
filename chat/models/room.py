from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from model_utils.models import UUIDModel

from .member import Member

channel_layer = get_channel_layer()


class Room(UUIDModel, models.Model):
    name = models.CharField(max_length=50, verbose_name='ルーム名')
    created_at = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False)

    def add_member(self, channel_name, user=None, is_online=False):
        return Member.objects.create(
            room=self,
            channel_name=channel_name,
            user=user,
        )

    @cached_property
    def members(self):
        return get_user_model().objects.filter(
            member__room=self,
        ).annotate(last_seen=models.Max('member__last_seen'))
