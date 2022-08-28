from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('myorders/', views.myorders, name="myorders"),
    path('myorders/<int:order_id>/', views.orderdetail, name="orderdetail"),
    path('Complete-order/<int:order_id>/',
         views.complete_order, name="complete_order"),

    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('main-dishes/', views.maindishes, name="maindishes"),
    path('side-dishes/', views.sidedishes, name="sidedishes"),
    path('desserts/', views.desserts, name="desserts"),

    path('waiter-portal/', views.waiterportal, name="waiterportal"),
    path('updateorder/<int:order_id>/', views.update_order, name="updateorder"),
]
