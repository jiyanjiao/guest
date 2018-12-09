from django.contrib import admin

# Register your models here.
from sign.models import Guest,Event
admin.site.register(Event)
admin.site.register(Guest)
