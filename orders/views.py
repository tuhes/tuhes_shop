from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from orders.models import Order, OrderItem
from orders.forms import OrderCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
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
