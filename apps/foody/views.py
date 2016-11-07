from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Dish, Chef, Buyer, Order, Message

# Create your views here.


def index(request):
    context = {
        "img": 123
    }

    return render(request, "index.html", context)


def buyer_or_chef(request):
    return render(request, 'buyer_or_chef.html')


def buyer_login_view(request):
    return render(request, 'buyer_login_registration.html')


def register_chef(request):
    """
    Author: DK
    Creates new chef profile in DB

    :param request
    :return:
    """
    username = request.POST.get("chef_name_register")
    email = request.POST.get("chef_email_register")
    password = request.POST.get("chef_pwd_register").encode()
    confirm_password = request.POST.get("chef_confirm_pwd_register").encode()
    error = False

    if Chef.chef_manager.validuser(username):
        messages.error(request, 'Username is not long enough!!', extra_tags='name')
        error = True

    if Chef.chef_manager.validemail(email):
        messages.error(request, 'Email is not valid', extra_tags='email')
        error = True

    if Chef.chef_manager.validpassword(password):
        messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password')
        error = True

    if Chef.chef_manager.matchpasswords(password, confirm_password):
        messages.error(request, 'Password Confirmation doesn\'t match!!', extra_tags='password_confirm')
        error = True

    if error:
        return redirect('/chef_login_view')
    else:
        Chef.chef_manager.register_chef(username, email, password)
        request.session['name'] = username
        return render(request, 'index.html')


def login_chef(request):
    """
    Author: DK
    Logs in chef

    :param request:
    :return:
    """
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
        return redirect('/chef_login_view')
    else:
        if Chef.chef_manager.login_chef(email, password):
            chef = Chef.chef_manager.filter(email=email).last()

            request.session['name'] = chef.username

            context = {
                "name": Chef.chef_manager.filter(email=email, password=password).last()
            }
            return redirect('/', context)
        else:
            messages.error(request, 'Your credentials does not match!', extra_tags='password_login')
            return redirect('/chef_login_view')


def chef_login_view(request):
    return render(request, 'chef_login_registration.html')


def register_buyer(request):
    """
    Author: DK
    Creates new chef profile in DB

    :param request, name, email, password, confirm_password:
    :return:
    """
    name = request.POST.get("buyer_name_register")
    email = request.POST.get("buyer_email_register")
    password = request.POST.get("buyer_pwd_register").encode()
    confirm_password = request.POST.get("buyer_confirm_pwd_register").encode()
    error = False

    if Buyer.buyer_manager.validuser(name):
        messages.error(request, 'Username is not long enough!!', extra_tags='name')
        error = True

    if Buyer.buyer_manager.validemail(email):
        messages.error(request, 'Email is not valid', extra_tags='email')
        error = True

    if Buyer.buyer_manager.validpassword(password):
        messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password')
        error = True

    if Buyer.buyer_manager.matchpasswords(password, confirm_password):
        messages.error(request, 'Password Confirmation doesn\'t match!!', extra_tags='password_confirm')
        error = True

    if error:
        return redirect('/buyer_login_view')
    else:
        Buyer.buyer_manager.register_buyer(name, email, password)
        request.session['name'] = name
        return render(request, 'index.html')


def login_buyer(request):
    """
    Author: DK
    Logs in chef

    :param request:
    :return:
    """
    error = False
    email = request.POST.get("buyer_email_login")
    password = request.POST.get('buyer_pwd_login').encode()

    if Buyer.buyer_manager.validemail(email):
        messages.error(request, 'Email is in the wrong format!', extra_tags='email_login')
        error = True
    if Buyer.buyer_manager.validpassword(password):
        messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password_login')
        error = True

    if error:
        return redirect('/buyer_login_view')
    else:
        if Buyer.buyer_manager.login_buyer(email, password):
            buyer = Buyer.buyer_manager.filter(email=email).last()

            request.session['name'] = buyer.name

            context = {
                "name": Buyer.buyer_manager.filter(email=email, password=password).last()
            }
            return redirect('/', context)
        else:
            messages.error(request, 'Your credentials does not match!', extra_tags='password_login')
            return redirect('/buyer_login_view')


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



def get_all_messages_inbox(request):
    if request.method == "POST":
        Message.objects.filter(reciever=request.user)
