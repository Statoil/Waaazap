from django.contrib.auth.models import User, Group
from models import HappynessRegistration, HappynessStatus
from rest_framework import serializers


class HappynessRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HappynessRegistration
        fields = ('device_id', 'timestamp', 'happyness_signal')



class HappynessStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HappynessStatus
        fields = 'sad_number', 'flat_number', 'good_number', 'happy_number'
