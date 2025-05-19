from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
from catalog.models import Item
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon


ORDER_STATUS_CHOICES = (
    ('active', 'Активный'),
    ('completed', 'Выполненный'),
    ('canceled', 'Отмененный')
)


class Order(models.Model):
#    first_name = models.CharField(max_length=50)
#    last_name = models.CharField(max_length=50)
#    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20,
                              choices=ORDER_STATUS_CHOICES,
                              default='active')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="промокод")
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id}'

    def get_total_cost(self):
        return sum(order_item.total_price() for order_item in self.orderitem_set.all())

    def get_discount(self):
        if self.discount > 0:
            return self.get_total_cost() * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost_with_discount(self):
        return self.get_total_cost() - self.get_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2,
                                validators=[MinValueValidator(1)])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def total_price(self):
        return self.price * self.quantity
