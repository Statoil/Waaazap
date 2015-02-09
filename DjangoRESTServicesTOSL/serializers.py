from django.contrib.auth.models import User, Group
from models import HappynessRegistration
from rest_framework import serializers


class HappynessRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HappynessRegistration
        fields = ('device_id', 'timestamp', 'happyness_signal')
