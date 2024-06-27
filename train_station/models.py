from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ForeignKey
from rest_framework.exceptions import ValidationError


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = ForeignKey("TrainType", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = ForeignKey("Journey",
                         on_delete=models.CASCADE,
                         related_name="tickets")
    order = ForeignKey("Order",
                       on_delete=models.CASCADE,
                       related_name="tickets")

    def __str__(self):
        return f"Ticket: {self.order} - {self.cargo} - {self.seat}"

    def validate_seat(self):
        max_seats = self.journey.train.places_in_cargo
        if not (1 <= self.seat <= max_seats):
            raise ValidationError(
                {
                    "seat": f"seat number must be in available range: (1, {max_seats})"
                }
            )

    def clean(self):
        super().clean()
        self.validate_seat()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



    class Meta:
        unique_together = ("cargo", "seat", "journey", "order")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_from"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_to"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f" Train {self.id}:"\
               f"{self.source.name} - {self.destination.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["destination", "source"], name="station_route"
            )
        ]


class Journey(models.Model):
    route = models.ForeignKey(Route,
                              on_delete=models.CASCADE,
                              related_name="journeys")
    train = models.ForeignKey(Train,
                              on_delete=models.CASCADE,
                              related_name="journeys")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.train}"

    @property
    def get_booked_seats(self):
        return self.tickets.values_list("seat", flat=True).distinct().count()


class Crew(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    position = models.CharField(max_length=150, blank=True)
    journey = models.ManyToManyField(Journey, blank=True, related_name="crews")

    @property
    def get_full_name_with_position(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

    def __str__(self):
        return self.first_name
