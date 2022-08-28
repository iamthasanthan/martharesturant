from django.db import models
from django.contrib.auth import get_user_model

from django.db.models.signals import post_save

from cart.models import UserCart

User = get_user_model()

USER_TYPES = [
    ('Customer', 'Customer'),
    ('Waitor', 'Waitor'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(
        upload_to='profilephoto/', null=True, blank=True, default='default.png')
    user_type = models.CharField(
        choices=USER_TYPES, blank=True, default='Customer', max_length=250)

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Profile(user=user)
            user_profile.save()
            user_cart = UserCart(user=user, quantity=0)
            user_cart.save()
    post_save.connect(create_profile, sender=User)

    def __str__(self):
        return self.user.username
