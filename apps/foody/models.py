from __future__ import unicode_literals
from django.db import models
import re
import datetime

now = datetime.datetime.now()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class BuyerManager(models.Manager):
    def logUser(self, username_in, pwd_in):
        error = False
        if len(username_in) < 2:
            error = True  # END OF EMAIL VALIDATION

        if len(pwd_in) < 8:
            error = True  # END OF PASSWORD VALIDATION

        if error is True:
            return False
        else:
            passwordHash = Buyer.BuyerManager.get(username=username_in).password.encode()
            if bcrypt.hashpw(pwd_in, passwordHash) == passwordHash:
                return True
            else:
                return False

    def regUser(self, username_up, email_up, pwd_up):
        error = []
        if len(username_up) < 2:
            # messages.error.extra_tags = 'username'
            error.append("Too short!! Username should be at least 2 characters")
        elif not username_up:
            error.append("Username field must be filled out")  # END OF FIRST NAME VALIDATION

        if not EMAIL_REGEX.match(email_up):
            error.append("Email is in wrong format")  # END OF EMAIL VALIDATION

        if len(pwd_up) < 8:
            error.append('Password is too short')
            # if pwd_up != passwordconf_up:
            # END OF PASSWORD VALIDATION
        if len(error) > 0:
            return [False, error]
        else:
            hashedPW = bcrypt.hashpw(pwd_up, bcrypt.gensalt())
            newuser = Buyer.BuyerManager.create(username=username_up, email=email_up, password=hashedPW, created_at=now)
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
        if len(pass_valid) < 9:
            return True
        else:
            return False

    def matchpasswords(self, password, confirmpass):
        if password != confirmpass:
            return True
        else:
            return False


class DishManager(models.Manager):
    def create_new_dish(self, dish_name, dish_description, dish_price, dish_photo_url, dish_chef_obj):
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
            error.append("Dish Photo must be filled out.")

        if len(error) > 0:
            return [False, error]
        else:
            newDish = Dish.dish_manager.create(name=dish_name,
                                               price=dish_price,
                                               description=dish_description,
                                               photo_url=dish_photo_url,
                                               belong_to_chef=dish_chef_obj,
                                               created_at=now,
                                               updated_at=now)
            return [True]


class Chef(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=25)
    credit_card = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    rating = models.FloatField(null=True, blank=True, default='5.0')
    photo = models.URLField(max_length=200)
    location = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chef_manager = BuyerManager()


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
    price = models.FloatField()
    dishes = models.ManyToManyField(Dish)

    STATE_CHOICES = (
        ('NS', 'NO_STATE'),
        ('PE', 'PENDING'),
        ('AP', 'APPROVED'),
        ('RJ', 'REJECTED'),
        ('DEL', 'DELIVERY'),
        ('FIN', 'FINAL'),
    )
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        default='NO_STATE',
    )

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    DELIVERY_CHOICES = (
        ('NS', 'NO_STATE'),
        ('CO', 'CARRY_OUT'),
        ('DE', 'DELIVERY'),
        ('BO', 'BOTH')
    )
    delivery_type = models.CharField(
        max_length=2,
        choices=DELIVERY_CHOICES,
        default='NO_STATE',
    )


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






