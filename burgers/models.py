from django.db import models
from django.contrib.auth.models import User

class BurgerOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    toppings = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order_number = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    burgers = models.CharField(max_length=200, default='')
    date_ordered = models.DateTimeField(auto_now_add=True)


class Burger(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)
    description = models.CharField(max_length=300, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=3)

    def __str__(self):
        return self.name


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
