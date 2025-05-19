from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from orders.models import Order, OrderItem
from catalog.models import Item
from coupons.models import Coupon
from orders.forms import OrderCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from orders.tasks import sent_email_after_order_created, sent_email_after_order_created_with_attachment

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            if cart.coupon:
                try:
                    coupon = Coupon.objects.get(id=cart.coupon)
                    order.coupon = coupon
                    order.discount = coupon.discount
                except Coupon.DoesNotExist:
                    order.coupon = None
                    order.discount = 0
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            sent_email_after_order_created_with_attachment.delay(order.id)
            return render(request, "orders/order/success.html",
                          context={'order': order})
    else:
        user = request.user
        initial = {'email': user.email,
                   'phone': user.profile.tel
                   }
        form = OrderCreationForm(initial=initial)
    return render(request, "orders/order/creates.html",
                  context={'form': form, 'cart': cart})


@require_POST
@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'active':
        order.status = 'canceled'
        order.save()
        return redirect('accounts:profile_view')
    else:
        return render(request, "orders/order/cancel_denied.html", {'order': order})


@login_required(login_url='accounts:login_view')
def order_detail(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=user)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'orders/order/detail.html', context=context)