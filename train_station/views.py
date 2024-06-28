from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from train_station.models import (Journey, Order, Route, Station, Ticket,
                                  Train, TrainType)
from train_station.serializers import (JourneyListSerializer,
                                       JourneySerializer, OrderListSerializer,
                                       OrderSerializer, RouteListSerializer,
                                       RouteSerializer, StationSerializer,
                                       TicketSerializer, TrainListSerializer,
                                       TrainRetrieveSerializer,
                                       TrainSerializer, TrainTypeSerializer)


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


class TicketModelView(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      ):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return TicketSerializer
        else:
            return TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user)


class OrderModelView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action in ("create"):
            return OrderSerializer
        elif self.action == "list":
            return OrderListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StationModelView(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteModelView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "create":
            return RouteSerializer
        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        source = self.request.query_params.get("source", None)
        destination = self.request.query_params.get("destination", None)
        if source:
            queryset = queryset.filter(
                source__name__icontains=source)
        if destination:
            queryset = queryset.filter(
                destination__name__icontains=destination)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                description="Find route by source station",
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        description='Find route with destination "Gare do Oriente"',
                    )
                ],
            ),
            OpenApiParameter(
                name="destination",
                description="Find route by destination station",
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        description='Find route with destination "Gare do Oriente"',
                    )
                ],
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class JourneyModelView(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action == "retrieve":
            return JourneySerializer
        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list"):
            queryset = queryset.annotate(
                holded=Count("tickets"),
                tickets_available=F("train__places_in_cargo") - F("holded"),
            )
            return queryset
        else:
            return queryset
