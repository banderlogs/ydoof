from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Dish

# Create your views here.


def index(request):
    context = {
        "img": 123
    }

    return render(request, "index.html", context)


def login_register(request):
    return render(request, '')


def add_dish(request):
    """
    Author: NP
    Used to add a dish

    :param request:
    :return:
    """
    if request.POST:
        dish_name = request.POST.get("dish_name")
        dish_description = request.POST.get("dish_description")
        dish_price = request.POST.get("dish_description")
        dish_photo_url = request.POST.get("dish_photo_url")
        dish_chef_obj = request.POST.get("dish_chef_obj")

        dish_err = Dish.dish_manager.create_new_dish(dish_name, dish_description,
                                                     dish_price, dish_photo_url,
                                                     dish_chef_obj)

        # If create_new_dish does not return an error
        if dish_err[0]:

            return render()
        else:
            messages.error(request, dish_err[1])

            return redirect('/add_dish')
    elif request.GET:
        return render(request, '/add_dish')

