from django.db import models
from foods.models import *
from django.contrib.auth import get_user_model

from django.db.models.signals import post_save

User = get_user_model()
# Create your models here.


class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    maindish = models.ManyToManyField(Maindish)
    sidedishes = models.ManyToManyField(Sidedish)
    desserts = models.ManyToManyField(Dessert, blank=True, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return self.user.username

    def __unicode__(self):
        return self.maindish
