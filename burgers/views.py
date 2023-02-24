from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Burger, BurgerOrder, BurgerOrderBurger
from .forms import BurgerOrderForm
import random
from django.shortcuts import get_object_or_404, render, redirect



def home(request):
    return render(request, 'burgers/templates/home.html')


# Function to calculate the price of a burger order
def calculate_price(toppings, quantity):
    # Base price of a burger is 5.99
    price = 5.99
    # Add 0.50 for each additional topping
    price += 0.50 * (len(toppings) - 1)
    # Multiply the price by the quantity
    price *= quantity
    # Round the price to two decimal places
    price = round(price, 2)
    return price


def generate_order_number():
    # Generate a random 6-digit number between 0 and 100
    order_number = random.randint(0, 100)
    # Check if the order number already exists in the database
    while BurgerOrder.objects.filter(order_number=order_number).exists():
        # If the order number already exists, generate a new one
        order_number = random.randint(0, 100)
    return order_number


@login_required
def order_burgers(request):
    if request.method == 'POST':
        form = BurgerOrderForm(request.POST)
        if form.is_valid():
            burger_order = form.save(commit=False)
            burger_order.order_number = generate_order_number()
            burger_order.save()
            for burger in form.cleaned_data['burger']:
                BurgerOrderBurger.objects.create(
                    burger=burger,
                    burger_order=burger_order
                )
            return redirect('view_order', order_number=burger_order.order_number)
    else:
        form = BurgerOrderForm()

    context = {
        'form': form,
        'burgers': Burger.objects.all(),
    }

    return render(request, 'burgers/order_burgers.html', context)


@login_required
def view_order(request, order_number):
    try:
        burger_order = BurgerOrder.objects.prefetch_related('burgerorderburger_set__burger').get(order_number=order_number)
    except BurgerOrder.DoesNotExist:
        raise Http404("Order does not exist")

    context = {
        'burger_order': burger_order,
    }

    return render(request, 'burgers/view_order.html', context)


def view_orders(request):
    orders = BurgerOrder.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'burgers/view_orders.html', context)

@login_required
def create_burger(request):
    if request.method == 'POST':
        form = BurgerOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_burgers')
    else:
        form = BurgerOrderForm()
    return render(request, 'burgers/create_burger.html', {'form': form})


@login_required
def edit_order(request, order_number):
    try:
        order = BurgerOrder.objects.get(order_number=order_number, customer_name=request.user)
    except BurgerOrder.DoesNotExist:
        return HttpResponse("This order does not exist.")

    burgers = order.burger_set.all()
    form = BurgerOrderForm(instance=order)
    if request.method == 'POST':
        form = BurgerOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('view_order', order_number=order_number)
    context = {
        'form': form,
        'order': order,
        'burgers': burgers,
    }
    return render(request, 'edit_order.html', context)


@login_required
def delete_order(request, order_number):
    try:
        order = BurgerOrder.objects.get(order_number=order_number, customer_name=request.user)
        order.delete()
        return redirect('view_orders')
    except BurgerOrder.DoesNotExist:
        # gérer le cas où l'objet n'existe pas
        return HttpResponse("Order does not exist.")


