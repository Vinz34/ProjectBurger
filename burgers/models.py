from django.db import models
from django.contrib.auth.models import User


class Burger(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)
    description = models.CharField(max_length=300, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=3)

    def __str__(self):
        return self.name


class BurgerOrder(models.Model):
    customer_name = models.CharField(max_length=100)
    order_number = models.IntegerField(default=0)
    burgers = models.ManyToManyField(Burger)
    date_created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.order_number} ({self.customer_name})"


class BurgerOrderBurger(models.Model):
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE)
    burger_order = models.ForeignKey(BurgerOrder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)





'''burger1 = Burger(name="Classic Cheeseburger", description="A classic cheeseburger with lettuce, tomato, pickles, and onions.", price=5.99)
burger1.save()
burger2 = Burger(name="Veggie Burger", description="A plant-based patty with lettuce, tomato, avocado, and sprouts.", price=6.99)
burger2.save()
burger3 = Burger(name="Bacon Cheeseburger", description="A classic cheeseburger with crispy bacon and barbecue sauce.", price=7.99)
burger3.save()
burger4 = Burger(name="Mushroom Swiss Burger", description="A juicy beef patty topped with sautéed mushrooms and Swiss cheese.", price=8.99)
burger4.save()
burger5 = Burger(name="Mushroom Swiss Burger", description="A juicy beef patty topped with sautéed mushrooms and Swiss cheese.", price=8.99)
burger5.save()'''
