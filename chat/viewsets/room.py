from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Room


class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'is_online']

    username = serializers.CharField(source='get_username')
    is_online = serializers.SerializerMethodField()

    def get_is_online(self, instance):
        return instance.last_seen > timezone.now() - timedelta(seconds=60)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'members']

    members = RoomMemberSerializer(many=True)


class RoomViewset(ReadOnlyModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects
