from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField("email", blank=True, max_length=254)
    description = models.TextField("опис користувача", null=True, max_length=500)


class Post(models.Model):
    title = models.CharField('заголовок поста', max_length=70)
    description = models.TextField("текст поста", max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="автор",
        on_delete=models.CASCADE,
        related_name="posts"
    )
    img = models.ImageField("зображеня", upload_to="image/users_media/posts_images/%Y", blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.author.username}'

    class Meta:
        verbose_name = 'Запис'
        verbose_name_plural = 'Записи'
