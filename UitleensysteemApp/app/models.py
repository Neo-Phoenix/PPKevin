from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Calendar(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.description}, Calendar ID: {self.id}"

class EventType(models.Model):
    type = models.CharField(max_length=255, unique=True)

    #python's dunder methode voor instance naam, nodig in admin om het leesbaar te houden zoals "uitlenen" aan ipv "EventType object (1)"
    def __str__(self):
        return f"{self.type}, EventType ID: {self.id}"

class ItemType(models.Model):
    type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.type}, ItemType ID: {self.id}"

class Item(models.Model):
    itemTypeID = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    naam = models.CharField(max_length=255, unique=True)
    beschrijving = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.naam}, Item ID: {self.id}"
    
class Event(models.Model):
    eventType = models.ForeignKey(EventType, on_delete=models.CASCADE)
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE)

    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        #f strings is handig voor string literals. eventType.type geeft onmiddelijk de naam die aan de FK zit
        return f"Event: {self.eventType.type}, Item ID: {self.itemid.naam}, Start: {self.start}, End: {self.end}, Event ID: {self.id}"


class CalendarEvent(models.Model):
    calendarid = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Calenderid: {self.calendarid} Event: {self.eventid}, CalendarEvent ID: {self.id}"