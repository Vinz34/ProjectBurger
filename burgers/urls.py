from django.urls import path

from .views import home, order_burgers, view_orders

urlpatterns = [
    #path('', views.index, name='home'),
    path('', home, name='home'),
    path('order-burgers/', order_burgers, name='order_burgers'),
    path('view-orders/', view_orders, name='view_orders'),
    path('<int:order_number>/', view_orders, name='view_orders'),
]