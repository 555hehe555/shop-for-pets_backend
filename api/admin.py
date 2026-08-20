from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    Cart,
    CustomUser,
    Product,
    ProductImage,
    Species,
    Category,
    Brand,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ["name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "is_available",

        "species",
        "category",
        "brand",

        "created_at",
    )
    list_filter = (
        "is_available",

        "species",
        "category",
        "brand",

        "created_at",
    )
    search_fields = (
        "title",
        "description",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "alt",
        "is_main",
    )
    list_filter = ("is_main",)
    search_fields = (
        "alt",
        "product__title",
    )

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" />', obj.image.url)
        return "-"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "quantity",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "user__username",
        "product__title",
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {"fields": ("description",)},
        ),
    )

    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
    )
