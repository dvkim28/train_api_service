from django.urls import include, path
from rest_framework import routers

from train_station.views import (
    OrderModelView,
    RouteModelView,
    StationModelView,
    TicketModelView,
    TrainModelView,
    TrainTypeModelView,
    JourneyModelView,
)

router = routers.DefaultRouter()
router.register("traintype", TrainTypeModelView)
router.register("train", TrainModelView)
router.register("station", StationModelView)
router.register("route", RouteModelView)
router.register("ticket", TicketModelView)
router.register("order", OrderModelView)
router.register("journey", JourneyModelView)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "train_station"
