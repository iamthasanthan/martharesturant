from django.db import models
from django.utils.text import slugify
# Create your models here.


class Maindish(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True)
    price = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to='maindish/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Maindish, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Sidedish(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True)
    price = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to='sidedish/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sidedish, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dessert(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True)
    price = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to='dessert/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Dessert, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
