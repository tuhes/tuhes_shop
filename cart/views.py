from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Item
from cart.cart import Cart
from cart.forms import CartAddItemForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item,
                 quantity=cd['quantity'],
                 override=cd['override'])
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    coupon_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart,
                                                                    'coupon_form': coupon_form})

@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:cart_detail')

@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')
