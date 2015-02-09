from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from models import HappynessRegistration
from serializers import HappynessRegistrationSerializer


class HappynessRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows HappynessRegistrations to be viewed or edited.
    """
    queryset = HappynessRegistration.objects.all()
    serializer_class = HappynessRegistrationSerializer
