from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Calendar(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class EventType(models.Model):
    type = models.CharField(max_length=255, unique=True)

    #python's dunder methode voor instance naam, nodig in admin om het leesbaar te houden zoals "uitlenen" aan ipv "EventType object (1)"
    def __str__(self):
        return self.type

class ItemType(models.Model):
    naam = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.naam

class Item(models.Model):
    itemTypeID = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    naam = models.CharField(max_length=255, unique=True)
    beschrijving = models.CharField(max_length=255)

    def __str__(self):
        return self.naam
class Event(models.Model):
    eventType = models.ForeignKey(EventType, on_delete=models.CASCADE)
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE)

    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        #f strings is handig voor string literals. eventType.type geeft onmiddelijk de naam die aan de FK zit
        return f"Event: {self.eventType.type}, Item ID: {self.itemid.naam}, Start: {self.start}, End: {self.end}"


class CalendarEvent(models.Model):
    calenderid = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Calender Event: {self.eventid}"