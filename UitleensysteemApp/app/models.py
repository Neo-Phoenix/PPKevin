from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    hashedpassword = models.CharField(max_length=255)

    @property
    def full_name(self):
        # Returns the person's full name.
        return f"{self.first_name} {self.last_name}"
    
    #python's dunder methode voor instance naam
    def __str__(self):
        return self.full_name

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