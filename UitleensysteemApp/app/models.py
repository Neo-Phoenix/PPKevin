from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Calendar(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

class Event(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()

    #python's dunder methode voor instance naam
    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    calenderid = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)