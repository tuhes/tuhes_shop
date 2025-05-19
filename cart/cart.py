from django.conf import settings
from decimal import Decimal
from catalog.models import Item
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon = self.session.get('coupon_id')

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]['product'] = item
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_coupon(self):
        if self.coupon:
            try:
                return Coupon.objects.get(id=self.coupon)
            except Coupon.DoesNotExist:
                pass
        return None

    def del_coupon(self):
        if self.coupon:
            del self.session['coupon_id']
            self.coupon = None
            self.save()

    def save(self):
        self.session.modified = True

    def add(self, item, quantity=1, override=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0,
                                     'price': str(item.price)}
        if override:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def clear(self):
        self.del_coupon()
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_discount(self):
        if self.coupon:
            return (self.get_coupon().discount / Decimal(100)) * self.get_total_price()
        return 0

    def get_total_price(self):
        total = sum(Decimal(item['price'] * item['quantity']) for item in self.cart.values())
        return total

    def get_total_price_with_discount(self):
        return self.get_total_price() - self.get_discount()