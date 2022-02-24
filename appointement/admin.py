from django.contrib import admin
from .models import Appointment, Reschedule, Notification
# Register your models here.
admin.site.register([Appointment, Reschedule, Notification])