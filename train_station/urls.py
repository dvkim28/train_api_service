from django.urls import path, include
from rest_framework import routers

from train_station.views import TrainTypeModelView

router = routers.DefaultRouter()
router.register("train_type", TrainTypeModelView)

urlpatterns = [
    path('', include(router.urls)),
]