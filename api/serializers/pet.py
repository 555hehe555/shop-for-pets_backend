from rest_framework import serializers

from ..models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ["id", "owner",  "name", "species", "birthday", "favourite_products"]
        read_only_fields = ("id", "owner")
        extra_kwargs = {"id": {"read_only": True}}
