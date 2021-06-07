from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils import timezone
from model_utils.models import UUIDModel


class MemberManager(models.Manager):
    def touch(self, channel_name, room_id=None):
        filter_q = Q(channel_name=channel_name)
        if room_id:
            filter_q &= Q(room_id=room_id)
        self.filter(filter_q).update(last_seen=timezone.now())


class Member(UUIDModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'channel_name'],
                name='unique_%(app_label)s_%(class)s_room_id_channel_name')]

    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    join_at = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)

    objects: MemberManager = MemberManager()

    def __str__(self):
        return self.channel_name
