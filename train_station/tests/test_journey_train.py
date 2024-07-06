from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from train_station.models import (
    Journey,
    Order,
    Route,
    Station,
    Ticket,
    Train,
    TrainType,
)
from train_station.serializers import JourneyListSerializer, JourneySerializer

JOURNEY_LIST = reverse("train_station:journey-list")
TRAIN_TYPE_LIST = reverse("train_station:traintype-list")
TRAIN_LIST = reverse("train_station:train-list")


def get_journey_detail(journey_pk):
    return reverse("train_station:journey-detail", args=[journey_pk])


def get_train_detail(train_pk):
    return reverse("train_station:train-detail", args=[train_pk])


def get_train_type_detail(train_type_pk):
    return reverse("train_station:train_type-detail", args=[train_type_pk])


def sample_ticket(**params):
    default = {
        "cargo": 1,
        "seat": 1,
        "journey": None,
        "order": None,
    }
    default.update(params)
    return Ticket.objects.create(**default)


def sample_order(user, **params):
    default = {
        "created_at": timezone.now(),
    }
    default.update(params)
    return Order.objects.create(user=user, **default)


def sample_journey(**params):
    default = {
        "route": None,
        "train": None,
        "departure_time": timezone.now(),
        "arrival_time": timezone.now(),
    }
    default.update(params)
    return Journey.objects.create(**default)


def sample_train_type(**params):
    default = {"name": "test type"}
    default.update(params)
    return TrainType.objects.create(**default)


def sample_train(**params):
    default = {
        "name": "test type",
        "cargo_num": 222,
        "places_in_cargo": 200,
    }
    default.update(params)
    return Train.objects.create(**default)


def sample_station(**params):
    default = {
        "name": "test station",
        "latitude": 200,
        "longitude": 200,
    }
    default.update(params)
    return Station.objects.create(**default)


def sample_route(**params):
    defaults = {"source": None, "destination": None, "distance": 10}
    defaults.update(params)
    return Route.objects.create(**defaults)


class UnAuthorizedTestCase(APITestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="PASSWORD",
            email="mail@test.com",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=None)
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="PASSWORD", email="mail2@test.com"
        )
        self.order1 = sample_order(user=self.user1)
        self.order2 = sample_order(user=self.user2)
        self.train1 = sample_train()
        self.station1 = sample_station()
        self.station2 = sample_station(
            name="real station",
        )
        self.route1 = sample_route(
            source=self.station1,
            destination=self.station2,
        )
        self.journey = sample_journey(
            route=self.route1,
            train=self.train1,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
        )

    def test_unauthorized_journey(self):
        response = self.client.get(JOURNEY_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_journey_detail(self):
        url = get_journey_detail(self.journey.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_train(self):
        response = self.client.get(TRAIN_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_train_detail(self):
        url = get_train_detail(self.train1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_train_type(self):
        response = self.client.get(TRAIN_TYPE_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedTestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="PASSWORD",
            email="mail@test.com",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="PASSWORD", email="mail2@test.com"
        )
        self.order1 = sample_order(user=self.user1)
        self.order2 = sample_order(user=self.user2)
        self.train1 = sample_train()
        self.station1 = sample_station()
        self.station2 = sample_station(
            name="real station",
        )
        self.route1 = sample_route(
            source=self.station1,
            destination=self.station2,
        )
        self.journey = sample_journey(
            route=self.route1,
            train=self.train1,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
        )

    def test_journey_list(self):
        jr = Journey.objects.all().annotate(
            holded=Count("tickets"),
            tickets_available=F("train__places_in_cargo") - F("holded"),
        )
        serializer = JourneyListSerializer(jr, many=True)
        response = self.client.get(JOURNEY_LIST)

        print("Response Data:", response.data)
        print("Serialized Data:", serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_journey_detail(self):
        sr_url = get_journey_detail(self.journey.id)
        serializer = JourneySerializer(self.journey)
        response = self.client.get(sr_url)
        self.assertEqual(response.data, serializer.data)

    def test_journey_post(self):
        data = {
            "route": self.route1.id,
            "train": self.train1.id,
            "departure_time": timezone.now(),
            "arrival_time": timezone.now(),
        }
        response = self.client.post(JOURNEY_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_journey_delete(self):
        url = get_journey_detail(self.journey.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_journey_update(self):
        data = {
            "route": self.route1.id,
            "train": self.train1.id,
            "departure_time": timezone.now(),
            "arrival_time": timezone.now(),
        }
        url = get_journey_detail(self.journey.id)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.journey.refresh_from_db()
        serializer = JourneySerializer(self.journey)
        self.assertEqual(serializer.data, response.data)
