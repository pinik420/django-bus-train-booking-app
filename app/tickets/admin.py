from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Busstop)
admin.site.register(Railway)
admin.site.register(Week)
admin.site.register(Train)
admin.site.register(Bus)
admin.site.register(Passenger)
admin.site.register(User)
admin.site.register(TrainTicket)
admin.site.register(BusTicket)