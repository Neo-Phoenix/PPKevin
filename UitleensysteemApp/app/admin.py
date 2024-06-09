from django.contrib import admin
from app.models import *

# Register your models here.
# usr: kevin
# psw: 12345678!

admin.site.register(EventType)
admin.site.register(Calendar)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Event)
admin.site.register(CalendarEvent)