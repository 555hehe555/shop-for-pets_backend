from rest_framework import serializers

from ..models import Product, ProductImage, Species


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "alt",
            "is_main",
        ]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    species = serializers.SlugRelatedField(slug_field="name", queryset=Species.objects.all(), required=False, allow_null=True)
    category = serializers.SlugRelatedField(slug_field="name", queryset=Species.objects.all(), required=False, allow_null=True)
    brand = serializers.SlugRelatedField(slug_field="name", queryset=Species.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "price",
            "discount",
            "is_available",

            "species",
            "category",
            "brand",

            "images",
        )
        read_only_fields = ("id", "created_at", "updated_at")
