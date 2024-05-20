from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import *

# Register your models here.
# usr: kevin
# psw: 12345678!

admin.site.register(User, UserAdmin)
admin.site.register(Calendar)
admin.site.register(Event)
admin.site.register(CalendarEvent)