from django.contrib import admin

from train_station.models import (
    Journey,
    Order,
    Route,
    Station,
    Ticket,
    Train,
    TrainType,
)

admin.site.register(Station)
admin.site.register(Train)
admin.site.register(TrainType)
admin.site.register(Route)
admin.site.register(Journey)
admin.site.register(Order)
admin.site.register(Ticket)
