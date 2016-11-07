from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime

now = datetime.datetime.now()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class ChefManager(models.Manager):
    def login_chef(self, email, password):
        """
        Author: NP
        Used to login the chef

        :param username: chef username
        :param password: chef password
        :return:
        """
        passwordHash = Chef.chef_manager.get(email=email).password.encode()

        if bcrypt.hashpw(password, passwordHash) == passwordHash:
            return True
        else:
            return False


    def register_chef(self, user_name, email, password):
        """
        Author: DK
        Used to register a new Chef

        :param user_name:
        :param email:
        :param password:
        :return:
        """
        hashedPW = bcrypt.hashpw(password, bcrypt.gensalt())
        Chef.chef_manager.create(username=user_name, email=email, password=hashedPW, created_at=now, updated_at=now)
        return [True]

    def validuser(self, username_valid):
        if len(username_valid) < 3:
            return True
        else:
            return False

    def validemail(self, email_valid):
        if not EMAIL_REGEX.match(email_valid):
            return True
        else:
            return False

    def validpassword(self, pass_valid):
        if len(pass_valid) < 8:
            return True
        else:
            return False

    def matchpasswords(self, password, confirm_password):
        if password != confirm_password:
            return True
        else:
            return False


class BuyerManager(models.Manager):
    def login_buyer(self, email, password):
        """
        Author: DK
        Used to login the buyer

        :param email: buyer username
        :param password: buyer password
        :return:
        """

        passwordHash = Buyer.buyer_manager.get(email=email).password.encode()

        if bcrypt.hashpw(password, passwordHash) == passwordHash:
            return True
        else:
            return False

    def register_buyer(self, username, email, password):
        """
        Author: NP
        Used to register a new Buyer

        :param username:
        :param email:
        :param password:
        :return: True/False
        """
        hashedPW = bcrypt.hashpw(password, bcrypt.gensalt())
        Buyer.buyer_manager.create(username=username, email=email, password=hashedPW, created_at=now, updated_at=now)
        return True

    def validuser(self, username_valid):
        if len(username_valid) < 3:
            return True
        else:
            return False

    def validemail(self, email_valid):
        if not EMAIL_REGEX.match(email_valid):
            return True
        else:
            return False

    def validpassword(self, pass_valid):
        if len(pass_valid) < 8:
            return True
        else:
            return False

    def matchpasswords(self, password, confirm_password):
        if password != confirm_password:
            return True
        else:
            return False


class DishManager(models.Manager):
    def create_new_dish(self, dish_name, dish_description, dish_price, dish_photo_url, dish_chef_obj):
        """
        Author: NP
        Creates and validates the new dish

        :param dish_name:
        :param dish_description:
        :param dish_price:
        :param dish_photo_url:
        :param dish_chef_obj:
        :return:
        """
        error = []

        if not dish_name:
            error.append("Dish name field must be filled out.")
        elif len(dish_name) < 3:
            error.append("Dish Name is too short. It must be more than 3 letters.")

        if not dish_description:
            error.append("Dish description must be filled out.")

        if not dish_price:
            error.append("Dish price must be filled out.")

        if not dish_photo_url:
            error.append("At least one Dish Photo must be submitted.")

        if len(error) > 0:
            return [False, error]
        else:
            Dish.dish_manager.create(name=dish_name,
                                     price=dish_price,
                                     description=dish_description,
                                     photo_url=dish_photo_url,
                                     belong_to_chef=dish_chef_obj,
                                     created_at=now,
                                     updated_at=now)
            return [True]


class OrderManager(models.Manager):
    def create_new_order(self, order_price, order_dishes, order_comment, order_delivery_options):

        error = []

        if not order_price:
            error.append("Order Price field must be filled out.")

        if not order_dishes:
            error.append("Dish Order field must be filled out.")

        if len(error) > 0:
            return [False, error]
        else:
            Order.order_manager.create(state='PENDING',
                                       delivery_type=order_delivery_options,
                                       price=order_price,
                                       dishes=order_dishes,
                                       comment=order_comment,
                                       created_at=now,
                                       updated_at=now)

            return [True]


class Chef(models.Model):
    username = models.CharField(max_length=60)
    address = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=25)
    credit_card = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=200, null=True)
    rating = models.FloatField(null=True, blank=True, default='5.0')
    photo = models.URLField(max_length=200, null=True)
    location = models.CharField(max_length=100, null=True)

    DELIVERY_CHOICES = (
        ('NS', 'NO_STATE'), ('CO', 'CARRY_OUT'),
        ('DE', 'DELIVERY'), ('BO', 'BOTH'),
    )
    delivery_type = models.CharField(
        max_length=2,
        choices=DELIVERY_CHOICES,
        default='NO_STATE',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chef_manager = ChefManager()


class Dish(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField()
    description = models.TextField()
    photo_url = models.URLField(max_length=200)
    belong_to_chef = models.ForeignKey(Chef)

    rating = models.FloatField(null=True, blank=True, default='5.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dish_manager = DishManager()


class Order(models.Manager):
    STATE_CHOICES = (
        ('NS', 'NO_STATE'), ('PE', 'PENDING'),
        ('AP', 'APPROVED'), ('RJ', 'REJECTED'),
        ('DEL', 'DELIVERY'), ('FIN', 'FINAL'),
    )
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        default='NO_STATE',
    )

    DELIVERY_CHOICES = (
        ('NS', 'NO_STATE'), ('CO', 'CARRY_OUT'),
        ('DE', 'DELIVERY'), ('BO', 'BOTH'),
    )
    delivery_type = models.CharField(
        max_length=2,
        choices=DELIVERY_CHOICES,
        default='NO_STATE',
    )

    price = models.FloatField()
    dishes = models.ManyToManyField(Dish)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_manager = OrderManager()


class Buyer(models.Model):
    username = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=25)
    fav_dishes = models.ManyToManyField(Dish)
    fav_chefs = models.ManyToManyField(Chef)
    credit_card = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    buyer_manager = BuyerManager()


class Message(models.Model):
    user_name_sender = models.OneToOneField(
        Buyer,
        on_delete=models.CASCADE
    )
    user_name_reciever = models.OneToOneField(
        Chef,
        on_delete=models.CASCADE,
    )
    send_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
