from django.db import transaction
from rest_framework import serializers

from train_station.models import (
    Journey,
    Order,
    Route,
    Station,
    Ticket,
    Train,
    TrainType,
    Crew,
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)

    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class TrainRetrieveSerializer(TrainSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)

    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class TrainListSerializer(TrainSerializer):
    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "cargo", "seat", "journey"]


class TicketRetrieveSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "cargo", "seat"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "tickets",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            tickets = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket in tickets:
                Ticket.objects.create(order=order, **ticket)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketRetrieveSerializer(many=True, read_only=False, allow_empty=False)
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "tickets"]


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class StationRetrieveSerializer(StationSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class StationListSerializer(StationSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = ["id", "source", "destination"]


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    crew_member = serializers.ReadOnlyField(source="get_full_name_with_position")

    class Meta:
        model = Crew
        fields = ["crew_member"]


class JourneyListSerializer(JourneySerializer):
    route = RouteListSerializer(many=False, read_only=True)
    train = TrainListSerializer(
        many=False,
        read_only=True,
    )
    booked_seats = serializers.SerializerMethodField()
    tickets_available = serializers.IntegerField(read_only=True)
    crews = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = [
            "id",
            "departure_time",
            "arrival_time",
            "booked_seats",
            "tickets_available",
            "route",
            "train",
            "crews",
        ]

    def get_booked_seats(self, obj):
        return obj.get_booked_seats


class JourneyRetrieveSerializer(JourneySerializer):
    class Meta:
        model = Journey
        fields = "__all__"
