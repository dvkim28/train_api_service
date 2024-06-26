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
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(
        source="train_type.name", read_only=True)

    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class TrainRetrieveSerializer(TrainSerializer):
    train_type = serializers.CharField(
        source="train_type.name", read_only=True)

    class Meta:
        model = Train
        fields = ["id",
                  "name",
                  "cargo_num",
                  "places_in_cargo",
                  "train_type"]


class TrainListSerializer(TrainSerializer):
    class Meta:
        model = Train
        fields = ["id",
                  "name",
                  "cargo_num",
                  "places_in_cargo",
                  "train_type"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "cargo", "seat", "journey"]


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False)
    user = serializers.ReadOnlyField(source="user.username")

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
    source = serializers.CharField(
        source="source.name", read_only=True)
    destination = serializers.CharField(
        source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(
        source="source.name", read_only=True)
    destination = serializers.CharField(
        source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"
