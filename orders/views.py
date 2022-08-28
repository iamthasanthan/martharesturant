import datetime
from django.shortcuts import render, redirect

from cart.models import UserCart
from foods.models import Dessert, Maindish, Sidedish
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderProduct
from django.contrib import messages

# Create your views here.


@login_required(login_url='login')
def place_order(request):
    current_user = request.user

    user_cart = UserCart.objects.filter(user=current_user).first()
    cart_count = user_cart.quantity
    if cart_count <= 0:
        return redirect('cart')

    grand_total = 0
    tax = 0
    total = 0
    if user_cart.maindish.count() > 0 and user_cart.sidedishes.count():
        for cart_item in user_cart.maindish.all():

            total += int(cart_item.price)
        for cart_item in user_cart.sidedishes.all():
            total += int(cart_item.price)
        for cart_item in user_cart.desserts.all():
            total += int(cart_item.price)
        # tax = (2 * total)/100
        grand_total = total + tax
        order = Order(
            user=request.user.profile,
            order_total=grand_total,
            tax=tax,

        )
        order.save()
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")  # 20210305
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()
        new_order = OrderProduct(
            user=request.user.profile,
            order=order,
            quantity=user_cart.quantity,
            product_price=grand_total,
        )
        new_order.save()
        for cart_item in user_cart.maindish.all():
            new_order.maindish.add(cart_item)
            user_cart.maindish.clear()

        for cart_item in user_cart.sidedishes.all():
            new_order.sidedishes.add(cart_item)
            user_cart.sidedishes.clear()
        for cart_item in user_cart.desserts.all():
            new_order.desserts.add(cart_item)
            user_cart.desserts.clear()
        new_order.save()

        user_cart.save()
    else:
        messages.error(
            request, "You must select any of Main dish and Side dish")

        return redirect('cart')

    return redirect('complete_order', new_order.id)
