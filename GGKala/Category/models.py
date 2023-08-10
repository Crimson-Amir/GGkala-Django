from django.db import models
from account.models import User
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html
from django.utils.formats import date_format
from django.urls import reverse


class CategoryManager(models.Manager):
    def return_truestatus(self):
        return self.filter(status="True")

    def published_categories(self):
        return self.filter(status="True", sexy_toys_related_name__publish="published", sexy_toys_related_name__inventory="available", parent__isnull=False).distinct()


class BrandManager(models.Manager):
    def return_truestatus(self):
        return self.filter(status="True")


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='parents_related')
    category_name = models.CharField(max_length=100)
    page_title = models.CharField(max_length=30, default="جی جی کالا")
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)
    caption = models.TextField(default="")
    photo = models.ImageField(upload_to="Category-photo", blank=True)

    class Meta:
        ordering = ['parent__id', 'id']

    def __str__(self):
        return self.category_name

    objects = CategoryManager()


def show_category(obj):
    return ", ".join([cat.category_name for cat in obj.category.return_truestatus()])


class Brand(models.Model):
    parent = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.SET_NULL, related_name='brand_related')
    brand_name = models.CharField(max_length=100)
    page_title = models.CharField(max_length=30, default="جی جی کالا")
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)
    caption = models.TextField(default="")
    photo = models.ImageField(upload_to="Brand-photo", blank=True)

    class Meta:
        ordering = ['parent__id', 'id']

    def __str__(self):
        return self.brand_name

    objects = BrandManager()


class Color(models.Model):
    STATUS = (("published", "PUBLISHED"), ("unpublished", "UNPUBLISHED"))
    color_name = models.CharField(max_length=50)
    color_rgb = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS, default="published")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.color_name