from django.urls import include, path
from rest_framework import routers

from train_station.views import (
    OrderModelView,
    RouteModelView,
    StationModelView,
    TicketModelView,
    TrainModelView,
    TrainTypeModelView,
)

router = routers.DefaultRouter()
router.register("train_type", TrainTypeModelView)
router.register("train", TrainModelView)
router.register("station", StationModelView)
router.register("route", RouteModelView)
router.register("ticket", TicketModelView)
router.register("order", OrderModelView)

urlpatterns = [
    path("", include(router.urls)),
]
