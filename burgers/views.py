from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import BurgerOrderForm
from .models import BurgerOrder
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order





def home(request):
    return render(request, 'burgers/home.html')

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

def order_burgers(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = BurgerOrderForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Get the toppings and quantity from the form data
            toppings = form.cleaned_data['toppings']
            quantity = form.cleaned_data['quantity']
            # Calculate the price of the order based on the toppings and quantity
            price = calculate_price(toppings, quantity)
            # Generate a unique order number
            order_number = generate_order_number()
            # Create a new BurgerOrder object with the current user, toppings, quantity, price, and order_number
            order = BurgerOrder(user=request.user, toppings=toppings, quantity=quantity, price=price, order_number=order_number)
            order.save()
            # Redirect the user to a page to view their orders
            return redirect('view_orders', order_number=order_number)
    else:
        # If the request is not a POST request, create a new form instance
        form = BurgerOrderForm()
    # Render the order_burgers.html template with the form
    return render(request, 'burgers/order_burgers.html', {'form': form})


# View for viewing orders
def view_orders(request, order_number):
    """
        Display the details of a specific order and allow the user to edit or delete it.
        """
    # Get the order with the specified order_number
    order = get_object_or_404(BurgerOrder, order_number=order_number)
    # Check if the user is authorized to view this order
    if request.user != order.user:
        return HttpResponseForbidden()

    # Check if the form has been submitted
    if request.method == 'POST':
        # Check if the user clicked the delete button
        if 'delete' in request.POST:
            # Delete the order and redirect to the view orders page
            order.delete()
            return redirect('view_orders')
        else:
            # Get the form data and update the order
            form = BurgerOrderForm(request.POST, instance=order)
            if form.is_valid():
                toppings = form.cleaned_data['toppings']
                quantity = form.cleaned_data['quantity']
                price = calculate_price(order.burger.price, toppings, quantity)

                # Update the order
                order.toppings = toppings
                order.quantity = quantity
                order.price = price
                order.save()

                return redirect('view_orders', order_number=order_number)
    else:
        # Create the form and pass in the current order instance
        form = BurgerOrderForm(instance=order)
        

    '''context = {'form': form, 'order': order}
    return render(request, 'burgers/view_orders.html', context)'''
    command = BurgerOrder.objects.get(order_number = order_number)

    context = {'command': command}
    return render(request, 'burgers/view_orders.html', context)

def edit_order(request, pk):
    # Retrieve the BurgerOrder object with the given primary key
    order = get_object_or_404(BurgerOrder, pk=pk)
    if request.method == 'POST':
        # If the form has been submitted, process the form data
        form = BurgerOrderForm(request.POST, instance=order)
        if form.is_valid():
            # Update the BurgerOrder object with the form data and save it
            order = form.save(commit=False)
            order.price = order.calculate_price()
            order.save()
            return redirect('view_orders')
    else:
        # If the form has not been submitted, create a new form with the current BurgerOrder object as the initial data
        form = BurgerOrderForm(instance=order)
    return render(request, 'edit_order.html', {'form': form, 'order': order})

def delete_order(request, pk):
    # Retrieve the BurgerOrder object with the given primary key
    order = get_object_or_404(BurgerOrder, pk=pk)
    # Delete the BurgerOrder object from the database
    order.delete()
    return redirect('view_orders')


