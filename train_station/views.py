from django.db.models import Count, F
from rest_framework import viewsets

from train_station.models import (
    Journey,
    Order,
    Route,
    Station,
    Ticket,
    Train,
    TrainType,
)
from train_station.serializers import (
    JourneySerializer,
    OrderSerializer,
    RouteListSerializer,
    RouteSerializer,
    StationSerializer,
    TicketSerializer,
    TrainListSerializer,
    TrainRetrieveSerializer,
    TrainSerializer,
    TrainTypeSerializer, JourneyListSerializer, JourneyRetrieveSerializer, OrderListSerializer,
)


class TrainTypeModelView(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainModelView(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        elif self.action == "retrieve":
            return TrainRetrieveSerializer
        else:
            return TrainSerializer


class TicketModelView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return TicketSerializer
        else:
            return TicketSerializer


class OrderModelView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return OrderSerializer
        elif self.action == "list":
            return OrderListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class StationModelView(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteModelView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer


class JourneyModelView(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action == "retrieve":
            return JourneyListSerializer
        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .annotate(
                    holded=Count("tickets"),
                    tickets_available=F("train__places_in_cargo")
                    - F("holded"),
                ))
            return queryset
