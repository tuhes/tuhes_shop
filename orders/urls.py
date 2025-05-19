from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:order_id>', views.order_cancel, name='order_cancel')
]