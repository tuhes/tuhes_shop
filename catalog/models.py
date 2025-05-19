from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MaxLengthValidator, MinLengthValidator


RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]


class Game(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='items/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ('name', '-created_at')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:item_detail', args=[self.id, self.slug])

    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0


class Review(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('item', 'user')

    def __str__(self):
        return f'Отзыв от {self.user.username}'
