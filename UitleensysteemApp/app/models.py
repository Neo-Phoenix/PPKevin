from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import PermissionsMixin



# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    identifier = models.CharField(max_length=40, unique=True)

    USERNAME_FIELD = "identifier"


    # @property
    # def full_name(self):
    #     # Returns the person's full name.
    #     return f"{self.first_name} {self.last_name}"
    
    # #python's dunder methode voor instance naam
    # def __str__(self):
    #     return self.full_name

class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email')

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