from django.shortcuts import render
from django.views.generic import ListView
from pip._vendor.rich.status import Status
from rest_framework import viewsets
from rest_framework.routers import Route

from train_station.models import TrainType, Train, Ticket, Order, Station, Journey
from train_station.serializers import TrainTypeSerializer, TrainSerializer, TicketSerializer, OrderSerializer, \
    StationSerializer, RouteSerializer, JourneySerializer


class TrainTypeModelView(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainModelView(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class TicketModelView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class OrderModelView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class StationModelView(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteModelView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class JourneyModelView(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer