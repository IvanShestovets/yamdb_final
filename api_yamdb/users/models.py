'''Переопределяем и расширяем стандартную модель пользователя.'''

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Админ'

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        default=UserRole.USER,
        choices=UserRole.choices,
    )

    def __str__(self) -> str:
        return f'{self.username}'

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email_pair'
            )
        ]
