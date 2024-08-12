from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    # Переопределяем поля first_name и last_name
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')

    # Добавляем related_name для полей groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Feedback(models.Model):
    feedback_name = models.CharField(max_length=50, verbose_name='Имя покупателя',)
    feedback_email = models.EmailField(verbose_name='Почта покупателя',)
    feedback_message = models.TextField(verbose_name='Текст',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',)

    class Meta:
        verbose_name = 'Обратная связь покупателя'
        verbose_name_plural = 'Обратная связь покупателя'

    def __str__(self):
        return self.feedback_message[:30]