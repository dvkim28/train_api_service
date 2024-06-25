from django.contrib import admin

from train_station.models import (
    Station,
    Train,
    TrainType,
    Route,
    Journey,
    Order
)

admin.site.register(Station)
admin.site.register(Train)
admin.site.register(TrainType)
admin.site.register(Route)
admin.site.register(Journey)
admin.site.register(Order)
