from django.db import models

class HappynessRegistration(models.Model):
    device_id = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    happyness_signal = models.CharField(max_length=20)

