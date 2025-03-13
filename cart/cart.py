from django.conf import settings
from decimal import Decimal
from catalog.models import Item


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

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
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        total = sum(Decimal(item['price'] * item['quantity']) for item in self.cart.values())
        return total