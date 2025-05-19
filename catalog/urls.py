from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:id>/<slug:slug>/', views.item_detail, name='item_detail'),
    path("addreview/<int:item_id>/", views.review_add, name='review_add'),
]