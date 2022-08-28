from django.shortcuts import render, redirect

from cart.models import UserCart
from foods.models import Dessert, Maindish, Sidedish
from django.contrib.auth.decorators import login_required
# Create your views here.


def viewcart(request):
    user_cart = UserCart.objects.filter(user=request.user).first()
    maindishes = Maindish.objects.filter(is_active=True).order_by('?')[:1]
    sidedishes = Sidedish.objects.filter(is_active=True).order_by('?')[:4]
    desserts = Dessert.objects.filter(is_active=True).order_by('?')[:4]

    context = {
        'maindishes': maindishes,
        'sidedishes': sidedishes,
        'desserts': desserts,
        'user_cart': user_cart,
    }
    return render(request, 'main/cart.html', context=context)


@login_required(login_url='login')
def add_cart(request, food_type, food_id):
    current_user = request.user
    user_cart = UserCart.objects.filter(user=current_user).first()
    if food_type == "maindish":
        dish = Maindish.objects.get(id=food_id)
        user_cart.maindish.add(dish)
        user_cart.save()
    elif food_type == "sidedish":
        dish = Sidedish.objects.get(id=food_id)
        user_cart.sidedishes.add(dish)
        user_cart.save()

    elif food_type == "dessert":
        dish = Dessert.objects.get(id=food_id)
        user_cart.desserts.add(dish)
        user_cart.save()

    return redirect('cart')


@login_required(login_url='login')
def remove_cart_item(request, food_type, food_id):
    current_user = request.user
    user_cart = UserCart.objects.filter(user=current_user).first()
    if food_type == "maindish":
        dish = Maindish.objects.get(id=food_id)
        user_cart.maindish.remove(dish)
        user_cart.save()
    elif food_type == "sidedish":
        dish = Sidedish.objects.get(id=food_id)
        user_cart.sidedishes.remove(dish)
        user_cart.save()

    elif food_type == "dessert":
        dish = Dessert.objects.get(id=food_id)
        user_cart.desserts.remove(dish)
        user_cart.save()
    return redirect('cart')

# def remove_cart(request, product_id, cart_item_id):
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(
#                 product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(
#                 product=product, cart=cart, id=cart_item_id)
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
#     return redirect('cart')
# def remove_cart_item(request, product_id, cart_item_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(
#             product=product, user=request.user, id=cart_item_id)
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(
#             product=product, cart=cart, id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart')
# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(
#                 user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         # tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass  # just ignore
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/cart.html', context)
# # @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(
#                 user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         # tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass  # just ignore
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context)
