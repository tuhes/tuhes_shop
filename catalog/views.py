from django.shortcuts import render, get_object_or_404
from catalog.models import Item, Category, Game
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddItemForm

def item_list(request):
    """
    Вывод всех товаров (в наличии)
    """
    items = Item.objects.filter(available=True).order_by('name')
    return render(request, 'item/list.html', context={'items': items})


@login_required(login_url='accounts:login_view')
def item_detail(request, id, slug):
    """
    Вывод отдельного товара (в наличии)
    """
    item = get_object_or_404(Item, id=id, slug=slug, available=True)
    cart_add_item_form = CartAddItemForm()
    return render(request, 'item/detail.html',
                  context={'item': item,
                           'cart_add_item_form': cart_add_item_form})

