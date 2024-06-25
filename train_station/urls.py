from django.urls import path, include
from rest_framework import routers

from train_station.views import TrainTypeModelView, TrainModelView, StationModelView, RouteModelView, OrderModelView, \
    TicketModelView

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
