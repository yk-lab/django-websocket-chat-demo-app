from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from model_utils.models import UUIDModel


class Room(UUIDModel, models.Model):
    name = models.CharField(max_length=50, verbose_name='ルーム名')
    created_at = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False)
