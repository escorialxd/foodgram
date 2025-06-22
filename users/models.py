from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    """Custom user model."""
    email = models.EmailField(
        'Email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        }
    )
    first_name = models.CharField('First name', max_length=150)
    last_name = models.CharField('Last name', max_length=150)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Subscription model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            UniqueConstraint(
                fields=["user", "author"], name="unique_subscription"
            )
        ]
