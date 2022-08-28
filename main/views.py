from django.shortcuts import render, redirect
from foods.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import get_user_model

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
