from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import CrewSerializer


class CrewRegisterView(generics.CreateAPIView):
    serializer_class = CrewSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CrewSerializer
    permission_classes = (IsAuthenticated,)


    def get_object(self):
        return self.request.user