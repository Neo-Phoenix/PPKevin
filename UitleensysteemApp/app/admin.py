from django.contrib import admin
from app.models import *

# Register your models here.
# usr: kevin
# psw: 12345678!

admin.site.register(User)
admin.site.register(Calendar)
admin.site.register(Event)
admin.site.register(CalendarEvent)