from django.contrib.auth import get_user_model
from rest_framework import serializers


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "is_staff", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
        }
        read_only_fields = ["id", "is_staff"]

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        crew = super().update(instance, validated_data)
        password = validated_data.pop("password", None)
        crew.set_password(password)
        if password:
            crew.set_password(password)
            crew.save()
        return crew
