import os
import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def product_image_path(instance, filename):
    ext = Path(filename).suffix
    return f"images/products/{instance.product.id}/{uuid.uuid4()}{ext}"

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"images/users_media/avatars/user_{instance.id}/{uuid.uuid4()}.{ext}"


class CustomUser(AbstractUser):
    email = models.EmailField("email", blank=True, max_length=254)
    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        blank=True
    )
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)


class Species(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Pet(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)

    favourite_products = models.ManyToManyField(Product, blank=True, related_name="favourite_products")


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to=product_image_path)
    image_medium = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    alt = models.CharField(max_length=255, blank=True)

    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.alt or f"Image #{self.pk}"

    def generate_thumbnails(self):
        if not self.image:
            return
            
        self.image.file.seek(0)
        img = Image.open(self.image.file)
        img_format = img.format if img.format else 'JPEG'
        
        if img_format == 'JPEG' and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        name, ext = os.path.splitext(self.image.name)
        
        img_medium = img.copy()
        img_medium.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        medium_io = BytesIO()
        img_medium.save(medium_io, format=img_format)
        self.image_medium.save(f"{name}_medium{ext}", ContentFile(medium_io.getvalue()), save=False)

        img_thumb = img.copy()
        img_thumb.thumbnail((300, 300), Image.Resampling.LANCZOS)
        thumb_io = BytesIO()
        img_thumb.save(thumb_io, format=img_format)
        self.image_thumbnail.save(f"{name}_thumb{ext}", ContentFile(thumb_io.getvalue()), save=False)
        
        self.image.file.seek(0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_instance = ProductImage.objects.filter(pk=self.pk).first() if not is_new else None

        if not is_new and old_instance and old_instance.image != self.image:
            if old_instance.image:
                old_instance.image.delete(save=False)
            if old_instance.image_medium:
                old_instance.image_medium.delete(save=False)
            if old_instance.image_thumbnail:
                old_instance.image_thumbnail.delete(save=False)

        if (is_new and self.image) or (old_instance and old_instance.image != self.image):
            self.generate_thumbnails()
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        if self.image_medium:
            self.image_medium.delete(save=False)
        if self.image_thumbnail:
            self.image_thumbnail.delete(save=False)
        super().delete(*args, **kwargs)


# class Product(models.Model):
#     title = models.CharField('заголовок поста', max_length=70)
#     description = models.TextField("текст поста", max_length=500)
#     price = models.IntegerField(verbose_name="ціна")
#     img = models.ImageField("зображення", upload_to="image/products_imgs/", blank=True)
#     is_available = models.BooleanField(verbose_name="в наявності", default=True)
#
#     def __str__(self):
#         return f'{self.title}'
#
#     class Meta:
#         verbose_name = 'Продукт'
#         verbose_name_plural = 'Продукти'
#
#
# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name="images"
#     )
#
#     alt = models.CharField(max_length=255)
#     is_main = models.BooleanField(default=False)
#     order = models.PositiveIntegerField(default=1)
#
#     image = models.ImageField(upload_to=f"image/products_imgs/{alt}/{order}")
#
#     def __str__(self):
#         return f'{self.alt}'
#
#     class Meta:
#         verbose_name = 'Картинка продукту'
#         verbose_name_plural = 'Картинки для продукту'


class Cart(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="carts",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        CustomUser,
        related_name="carts",
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1, blank=False, null=False, validators=[MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_cart",
            )
        ]
