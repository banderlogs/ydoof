from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Dish, Chef, Buyer, Order

# Create your views here.


def index(request):
    context = {
        "img": 123
    }

    return render(request, "index.html", context)


def login_register(request):
    return render(request, 'Login_Registration.html')


def register_chef(request):
    name = request.POST.get("chef_name_reg")
    email = request.POST.get("chef_email_reg")
    password = request.POST.get("chef_pwd_reg").encode()
    confirm_password = request.POST.get("chef_confirm_pwd_reg").encode()
    error = False

    if Chef.chef_manager.validuser(name):
        messages.error(request, 'Username is not long enough!!', extra_tags='name')
        error = True

    if Chef.chef_manager.validemail(email):
        messages.error(request, 'Email is not valid', extra_tags='email')
        error = True

    if Chef.chef_manager.validemail(password):
        messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password')
        error = True

    if Chef.chef_manager.matchpasswords(password, confirm_password):
        messages.error(request, 'Password Confirmation doesn\'t match!!', extra_tags='password_confirm')
        error = True

    if error:
        return redirect('/')
    else:
        Chef.chef_manager.registerChef(name, email, password)
        request.session['name'] = name
        return render(request, 'index.html')


def login_chef(request):
    error = False
    email = request.POST.get("chef_email_login")
    password = request.POST.get('chef_pwd_login').encode()

    if Chef.chef_manager.validemail(email):
        messages.error(request, 'Email is in the wrong format!', extra_tags='email_login')
        error = True
    if Chef.chef_manager.validpassword(password):
        messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password_login')
        error = True

    if error:
        return redirect('/login')
    else:
        Chef.chef_manager.login_chef(email, password)
        chef = Chef.chef_manager.filter(email=email).last()

        request.session['name'] = chef.name

        context = {
            "name": Chef.chef_manager.filter(email=email, password=password).last()
        }
        return redirect('/', context)



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

