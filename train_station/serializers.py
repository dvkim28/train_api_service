from rest_framework import serializers

from train_station.models import TrainType, Train, Ticket, Order, Station, Route, Journey


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = '__all__'


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'