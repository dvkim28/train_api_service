from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets

from train_station.models import TrainType
from train_station.serializers import TrainTypeSerializer


class TrainTypeModelView(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
