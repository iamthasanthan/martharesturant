from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('main-dishes/', views.maindishes, name="maindishes"),
    path('side-dishes/', views.sidedishes, name="sidedishes"),
    path('desserts/', views.desserts, name="desserts"),
]
