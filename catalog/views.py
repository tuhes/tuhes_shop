from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Item, Category, Game, Review
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddItemForm
from django.core.cache import caches
from django.conf import settings
from django.db.models import Case, When, IntegerField
from django.views.decorators.http import require_POST
from orders.models import OrderItem
from catalog.forms import ReviewForm


VIEWS_CACHE = caches["views"]


def item_views_tracker(item_id):
    redis_client = VIEWS_CACHE.client.get_client()
    key = f"{settings.ITEM_VIEW}:{item_id}"

    redis_client.incr(key)

    redis_client.zincrby(settings.TOP_VIEWS, 1, item_id)

    return int(redis_client.get(key))


def get_item_top_views(limit=settings.TOP_VIEWS_LIMIT):
    redis_client = VIEWS_CACHE.client.get_client()
    top = redis_client.zrevrange(settings.TOP_VIEWS, 0, limit - 1, withscores=False)

    return [int(item) for item in top]


def item_list(request):
    """
    Вывод всех товаров (в наличии)
    """
    items = Item.objects.filter(available=True).order_by('name')
    top_item_ids = get_item_top_views()

    preserved = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(top_item_ids)])
    items_top = Item.objects.filter(id__in=top_item_ids).order_by(preserved)

    return render(request, 'item/list.html',
                  context={'items': items, 'items_top': items_top})


@login_required(login_url='accounts:login_view')
def item_detail(request, id, slug):
    """
    Вывод отдельного товара (в наличии) + счётчик просмотров
    """
    item = get_object_or_404(Item, id=id, slug=slug, available=True)

    view_count = item_views_tracker(item.id)
    cart_add_item_form = CartAddItemForm()

    reviews = Review.objects.filter(item=item).order_by('-created_at')

    can_review = False
    review_form = None

    if request.user.is_authenticated:
        has_ordered = OrderItem.objects.filter(
            order__user=request.user,
            item=item,
            order__status="completed"
        ).exists()

        existing_review = item.reviews.filter(user=request.user).exists()

        if has_ordered and not existing_review:
            can_review = True
            review_form = ReviewForm()

    return render(request, 'item/detail.html',
                  context={'item': item,
                           'view_count': view_count,
                           'cart_add_item_form': cart_add_item_form,
                           'can_review': can_review,
                           'review_form': review_form,
                           'reviews': reviews})


@require_POST
def review_add(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.user.is_authenticated:
        has_ordered = OrderItem.objects.filter(
            order__user=request.user,
            item=item,
            order__status="completed"
        ).exists()

        if not has_ordered:
            return redirect('catalog:item_detail', id=item_id, slug=item.slug)

        existing_review = item.reviews.filter(user=request.user).exists()
        if existing_review:
            return redirect('catalog:item_detail', id=item_id, slug=item.slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()

    return redirect('catalog:item_detail', id=item_id, slug=item.slug)
