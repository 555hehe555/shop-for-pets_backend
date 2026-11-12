from rest_framework import serializers

from .product import ProductSerializer
from ..models import FavouriteProduct


class FavouriteProductSerializer(serializers.ModelSerializer):
    product_data = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = FavouriteProduct
        fields = [
            "product",
            "product_data",
            "created_at",
        ]
        read_only_fields = [
            "created_at",
        ]
