from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from train_station.models import (
    Ticket,
    Order,
    Journey,
    TrainType,
    Train,
    Station,
    Route
)
from train_station.serializers import TicketSerializer

TICKET_LIST_URL = reverse("train_station:ticket-list")


def get_ticket_retrieve_url(ticket_id):
    return reverse("train_station:ticket-detail", args=[ticket_id])


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
    default = {
        "name": "test type"
    }
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
    defaults = {
        "source": None,
        "destination": None,
        "distance": 10
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


class UnAuthorizedTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=None)

    def test_unauthorized_ticket_list(self):
        response = self.client.get(TICKET_LIST_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_ticket_detail(self):
        response = self.client.get(get_ticket_retrieve_url(1))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class AuthorizedTestCase(APITestCase):
    def setUp(self):
        self.user1 = (get_user_model().objects.create_user(
            username="user1",
            password="PASSWORD",
            email="mail@test.com"
        ))
        self.client = APIClient()
        (self.client.
         force_authenticate(user=self.user1))
        self.user2 = (get_user_model().objects.create_user(
            username="user",
            password="PASSWORD",
            email="mail2@test.com"
        ))
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
            arrival_time=timezone.now()
        )

    def test_ticket_list(self):
        tk1 = sample_ticket(
            cargo=1,
            seat=1,
            journey=self.journey,
            order=self.order1
        )
        tk2 = sample_ticket(
            cargo=2,
            seat=2,
            journey=self.journey,
            order=self.order2
        )
        serializer1 = TicketSerializer(tk1)
        serializer2 = TicketSerializer(tk2)
        response = self.client.get(TICKET_LIST_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertIn(serializer1.data,
                      response.data)
        self.assertNotIn(serializer2.data,
                         response.data)

    def test_ticket_detail(self):
        tk1 = sample_ticket(
            cargo=1,
            seat=1,
            journey=self.journey,
            order=self.order1)
        serializer = TicketSerializer(tk1)
        response = self.client.get(
            get_ticket_retrieve_url(tk1.id)
        )
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_ticket_create(self):
        data = {
            "cargo": 1,
            "seat": 1,
            "journey": self.journey.id,
            "order": self.order1.id,
        }
        response = (self.client.
                    post(TICKET_LIST_URL, data))
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_ticket_update(self):
        updated = {
            "cargo": 8,
        }
        data = {
            "cargo": 1,
            "seat": 1,
            "journey": self.journey.id,
            "order": self.order1.id,
        }
        response = (self.client.
                    post(TICKET_LIST_URL, data))
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        url = get_ticket_retrieve_url(response.data["id"])
        response = self.client.put(url, updated)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ticket_delete(self):
        tk = sample_ticket(
            cargo=1,
            seat=1,
            journey=self.journey,
            order=self.order1,
        )
        response = (self.client.delete
                    (get_ticket_retrieve_url(tk.id)))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
