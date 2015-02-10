from django.db import models

class HappynessRegistration(models.Model):
    device_id = models.CharField(max_length=200)
    timestamp = models.DateTimeField(blank=True)
    mood = models.CharField(max_length=20)

class HappynessStatus(models.Model):
    sad_number = models.IntegerField()
    flat_number = models.IntegerField()
    good_number = models.IntegerField()
    happy_number = models.IntegerField()