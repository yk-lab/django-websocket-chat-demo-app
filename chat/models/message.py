from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel

from .room import Room


class Message(UUIDModel, models.Model):
    room = models.ForeignKey(
        Room,
        related_name='messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False)
