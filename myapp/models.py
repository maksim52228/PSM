from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"Image for {self.news.title}"
class Application(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    description = models.TextField('Описание проблемы', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return f'Заявка от {self.name}'


class ChatMessage(models.Model):
    username = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.username}: {self.message[:20]}...'

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя сотрудника")
    position = models.CharField(max_length=100, verbose_name="Должность")
    photo = models.ImageField(upload_to='employees/', verbose_name="Фото")
    bio = models.TextField(verbose_name="Краткая информация", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['order', 'name']

    def clean(self):
        # Пример валидации - проверка, что имя не пустое
        if not self.name.strip():
            raise ValidationError(_('Имя сотрудника не может быть пустым'))

    def save(self, *args, **kwargs):
        # Можно добавить автоматическую обработку перед сохранением
        self.name = self.name.strip()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
class Works(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Название объекта")
    photo = models.ImageField(upload_to='works/', verbose_name="Фото")
    bio = models.TextField(verbose_name="Информация", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Наши работы"
        ordering = ['order', '-created_at']

    def clean(self):
        # Пример валидации - проверка, что имя не пустое
        if not self.name.strip():
            raise ValidationError(_('Название объекта не может быть пустым'))

    def save(self, *args, **kwargs):
        # Можно добавить автоматическую обработку перед сохранением
        self.name = self.name.strip()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

