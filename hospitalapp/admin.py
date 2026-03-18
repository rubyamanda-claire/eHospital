from django.contrib import admin

from hospitalapp.models import *


# Register your models here.
admin.site.register(Patient)

admin.site.register(Doctor)

admin.site.register(MyAppointment)

admin.site.register(Transaction)
