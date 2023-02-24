from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('order-burgers/', views.order_burgers, name='order_burgers'),
    path('view-orders/', views.view_orders, name='view_orders'),
    path('view-order/<int:order_number>/', views.view_order, name='view_order'),
    path('<int:order_number>/edit/', views.edit_order, name='edit_order'),
    path('<int:order_number>/delete/', views.delete_order, name='delete_order'),
]