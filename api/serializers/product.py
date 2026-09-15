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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        view = self.context.get('view')
        
        file_field = instance.image
        if view and hasattr(view, 'action'):
            if view.action == 'list':
                file_field = instance.image_thumbnail or instance.image
            elif view.action in ['retrieve', 'update', 'partial_update']:
                file_field = instance.image_medium or instance.image
                
        if file_field:
            url = file_field.url
            if request is not None:
                url = request.build_absolute_uri(url)
            data['image'] = url
        else:
            data['image'] = None
            
        return data


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
