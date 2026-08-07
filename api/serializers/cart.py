from rest_framework import serializers

from .product import ProductSerializer
from ..models import Cart


class CartSerializer(serializers.ModelSerializer):
    product_data = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Cart
        fields = [
            "product",
            "product_data",
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
