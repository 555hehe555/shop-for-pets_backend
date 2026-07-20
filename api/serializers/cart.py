from rest_framework import serializers

from ..models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "product",
            "quantity",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class CartPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["quantity"]
