from django.contrib import admin

# Register your models here.
from appointments.models import Appointment

admin.site.register(Appointment)