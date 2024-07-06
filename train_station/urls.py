from django.urls import include, path
from rest_framework import routers

from train_station.views import (
    JourneyModelView,
    OrderModelView,
    RouteModelView,
    StationModelView,
    TicketModelView,
    TrainModelView,
    TrainTypeModelView,
)

router = routers.DefaultRouter()
router.register("traintypes", TrainTypeModelView)
router.register("trains", TrainModelView)
router.register("stations", StationModelView)
router.register("routes", RouteModelView)
router.register("tickets", TicketModelView)
router.register("orders", OrderModelView)
router.register("journeys", JourneyModelView)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "train_station"
