from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True, verbose_name="Промокод")
    valid_from = models.DateTimeField(verbose_name="Начала действия", blank=True, null=True)
    valid_to = models.DateTimeField(verbose_name="Конец действия купона", blank=True, null=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    active = models.BooleanField(default=True)
    usage = models.IntegerField(default=0)
    max_usage = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
