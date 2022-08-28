from django.shortcuts import render, redirect
from foods.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import get_user_model
from orders.models import Order, OrderProduct

from users.models import Profile


User = get_user_model()

# Create your views here.


def logout(request):
    auth.logout(request)
    return redirect('login')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():

            c_user = User.objects.get(email=email)
            user = auth.authenticate(
                username=c_user.username, password=password)
            # user.backend = 'django.contrib.auth.backends.ModelBackend'

            auth.login(request, user)

            messages.info(request, f"You are now logged in with {email}.")
            return redirect("home")

    context = {}
    return render(request, 'main/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        phone = request.POST['phone']
        if not (User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists()):

            user = User.objects.create_user(
                email=email, username=username, password=password
            )
            cuser = auth.authenticate(
                username=username, password=password)
            profile = Profile.objects.get(user=user)
            profile.phone_number = phone
            profile.save()
            auth.login(request, cuser)
            print(user)
            # auth_login(request, user)
            messages.success(request, 'Account succesfully created')
            return redirect("home")
        else:
            messages.error(
                request, f"You are already have an account, Login!")
    context = {}
    return render(request, 'main/register.html', context)


def index(request):
    maindishes = Maindish.objects.filter(is_active=True).order_by('?')[:3]
    sidedishes = Sidedish.objects.filter(is_active=True).order_by('?')[:4]
    desserts = Dessert.objects.filter(is_active=True).order_by('?')[:4]

    context = {
        'maindishes': maindishes,
        'sidedishes': sidedishes,
        'desserts': desserts,
    }
    return render(request, 'main/index.html', context=context)


def maindishes(request):
    maindishes = Maindish.objects.filter(is_active=True)
    context = {
        'maindishes': maindishes,
    }
    return render(request, 'main/maindishes.html', context=context)


def desserts(request):
    desserts = Dessert.objects.filter(is_active=True)
    context = {
        'desserts': desserts,
    }
    return render(request, 'main/desserts.html', context=context)


def sidedishes(request):
    sidedishes = Sidedish.objects.filter(is_active=True)
    context = {
        'sidedishes': sidedishes,
    }
    return render(request, 'main/sidedishes.html', context=context)


@login_required(login_url='login')
def myorders(request):
    myorders = OrderProduct.objects.filter(
        user=request.user.profile).order_by('-created_at')
    context = {
        'myorders': myorders,
    }
    return render(request, 'main/myorders.html', context=context)


@login_required(login_url='login')
def orderdetail(request, order_id):
    order = OrderProduct.objects.filter(
        id=order_id).first()
    context = {
        'order': order,
    }
    return render(request, 'main/orderdetail.html', context=context)


@login_required(login_url='login')
def complete_order(request, order_id):
    order_p = OrderProduct.objects.filter(id=order_id).first()
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        order_note = request.POST.get('order_note')
        order = order_p.order
        order.first_name = first_name
        order.last_name = last_name
        order.email = email
        order.phone = phone
        order.address_line_1 = address_line_1
        order.address_line_2 = address_line_2
        order.order_note = order_note
        order.status = "Ordered"
        order.save()
        order_p.ordered = True
        order_p.save()
        return redirect('myorders')
    context = {
        'order': order_p,
    }
    return render(request, 'main/completeorder.html', context=context)


@login_required(login_url='login')
def waiterportal(request):
    if request.user.profile.user_type == "Waitor":
        orders = OrderProduct.objects.exclude(
            order__status="New").order_by('-created_at')
        context = {
            'orders': orders,
        }
        return render(request, 'main/waiterdashboard.html', context=context)
    else:
        return redirect('home')


@login_required(login_url='login')
def update_order(request, order_id):
    if request.user.profile.user_type == "Waitor":
        order_p = OrderProduct.objects.get(id=order_id)
        if request.method == "POST":
            status = request.POST.get('status')
            order = Order.objects.filter(id=order_p.order.id).first()
            order.status = status
            order.save()
        return redirect('waiterportal')
    else:
        return redirect('home')
