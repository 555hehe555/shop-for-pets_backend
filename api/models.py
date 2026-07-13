from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import uuid
from pathlib import Path


def product_image_path(instance, filename):
    ext = Path(filename).suffix
    return f"products/{instance.product.id}/{uuid.uuid4()}{ext}"


class CustomUser(AbstractUser):
    email = models.EmailField("email", blank=True, max_length=254)
    description = models.TextField("опис користувача", null=True, max_length=500)


class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to=product_image_path)

    alt = models.CharField(max_length=255, blank=True)

    is_main = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    def str(self):
        return self.alt or f"Image #{self.pk}"

# class Product(models.Model):
#     title = models.CharField('заголовок поста', max_length=70)
#     description = models.TextField("текст поста", max_length=500)
#     price = models.IntegerField(verbose_name="ціна")
#     img = models.ImageField("зображеня", upload_to="image/products_imgs/", blank=True)
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
