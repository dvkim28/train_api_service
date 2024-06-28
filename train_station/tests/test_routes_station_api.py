from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from train_station.models import Route, Station, Train, TrainType
from train_station.serializers import RouteListSerializer, RouteSerializer

ROUTES_URL = reverse("train_station:route-list")
STATIONS_URL = reverse("train_station:station-list")


def sample_train_type(**params):
    default = {"name": "test type"}
    default.update(params)
    return TrainType.objects.create(**default)


def get_route_retrieve_url(route_id):
    return reverse("train_station:route-detail", args=[route_id])


def get_station_retrieve_url(station_id):
    return reverse("train_station:station-detail", args=[station_id])


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


class UnAuthorizedRoutesAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_routes_list(self):
        response = self.client.get(ROUTES_URL)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_unauthorized_routes_detail(self):
        train_type = sample_train_type()
        train1 = sample_train(train_type=train_type)
        url = get_route_retrieve_url(train1.id)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class AuthorizedRoutesAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="PASSWORD",
            is_staff=False,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.station1 = sample_station(
            name="test station",
        )
        self.station2 = sample_station(
            name="real station",
        )

    def test_routes_list(self):
        Route.objects.create(
            destination=self.station1,
            source=self.station2,
            distance=10,
        )
        Route.objects.create(
            destination=self.station2,
            source=self.station1,
            distance=10,
        )
        response = self.client.get(ROUTES_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_routes_detail(self):
        route = Route.objects.create(
            destination=self.station1,
            source=self.station2,
            distance=10,
        )
        url = reverse("train_station:route-detail", args=[route.id])
        response = self.client.get(url)
        serializer = RouteSerializer(route)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_routes_filter_by_source(self):
        route = Route.objects.create(
            destination=self.station1,
            source=self.station2,
            distance=10,
        )
        route2 = Route.objects.create(
            destination=self.station2,
            source=self.station1,
            distance=10,
        )
        url = reverse("train_station:route-list")
        response = self.client.get(url, {"source": self.station2.name})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer = RouteListSerializer(
            route,
        )
        self.assertIn(serializer.data, response.data)
        serializer = RouteListSerializer(
            route2,
        )
        self.assertNotIn(serializer.data, response.data)

    def test_route_delete(self):
        route = Route.objects.create(
            destination=self.station1,
            source=self.station2,
            distance=10,
        )
        url = reverse("train_station:route-detail", args=[route.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_create(self):
        response = self.client.post(
            ROUTES_URL,
            {"destination": self.station1, "source": self.station2, "distance": 10},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_update(self):
        route = Route.objects.create(
            destination=self.station1,
            source=self.station2,
            distance=10,
        )
        url = reverse("train_station:route-detail", args=[route.id])
        response = self.client.put(url, {"distance": 100})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_station_create(self):
        response = self.client.post(
            STATIONS_URL,
            {
                "name": "test station",
                "latitude": 200,
                "longitude": 200,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_station_update(self):
        station = Station.objects.create(
            name="test station",
            latitude=200,
            longitude=200,
        )
        url = get_station_retrieve_url(station.id)
        response = self.client.put(
            url,
            {
                "name": "test station2",
                "latitude": 200,
                "longitude": 200,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_station_delete(self):
        station = Station.objects.create(
            name="test station",
            latitude=200,
            longitude=200,
        )
        url = get_station_retrieve_url(station.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAuthorizedRoutesAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="PASSWORD",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.station1 = sample_station()
        self.station2 = sample_station(
            name="real station",
        )

    def test_routes_post(self):
        response = self.client.post(
            ROUTES_URL,
            {
                "destination": self.station1.id,
                "source": self.station2.id,
                "distance": 10,
            },
        )
        route = Route.objects.get(id=response.data["id"])
        serializer = RouteSerializer(route)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data, serializer.data)

    def test_routes_patch(self):
        response = self.client.post(
            ROUTES_URL,
            {
                "destination": self.station1.id,
                "source": self.station2.id,
                "distance": 10,
            },
        )
        route = Route.objects.get(id=response.data["id"])
        serializer = RouteSerializer(route)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data, serializer.data)
        url = reverse("train_station:route-detail", args=[route.id])
        response = self.client.patch(
            url,
            {
                "destination": self.station2.id,
                "source": self.station2.id,
                "distance": 22,
            },
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        route.refresh_from_db()
        serializer = RouteSerializer(route)
        self.assertEqual(response.data, serializer.data)

    def test_routes_delete(self):
        station1 = sample_station()
        station2 = sample_station()
        route = Route.objects.create(
            destination=station1,
            source=station2,
            distance=10,
        )
        url = reverse("train_station:route-detail", args=[route.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_station_delete(self):
        station1 = sample_station()
        url = get_station_retrieve_url(station1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_station_create(self):
        response = self.client.post(
            STATIONS_URL,
            {
                "name": "test station",
                "latitude": 200,
                "longitude": 200,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_station_update(self):
        station = Station.objects.create(
            name="test station",
            latitude=200,
            longitude=200,
        )
        url = get_station_retrieve_url(station.id)
        response = self.client.put(
            url,
            {
                "name": "test station2",
                "latitude": 200,
                "longitude": 200,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
