from django.db import models
from account.models import User, ViewCounter
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html
from django.utils.formats import date_format
from django.urls import reverse
from Category.models import Category, Color, Brand
from django.contrib.contenttypes.fields import GenericRelation
from review.models import ReviewModel


class MyManager(models.Manager):

    def return_published_product(self):
        return self.filter(publish="published")


def get_absolute_url():
    return reverse("account:products")


class SexToys(models.Model):
    INVENTORY = (("available", "موجود"),
                 ("unavailable", "ناموجود"))
    PUBLISHD = (("published", "منتشر شده"),
                ("unpublished", "پیش نویس"),
                ("pending", "درحال بررسی"),
                ("returned", "برگشت داده شده"),)

    publisher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="publisher_Products", verbose_name="اضافه کننده")
    title = models.TextField(max_length=65, verbose_name="عنوان")
    photo = models.ImageField(upload_to="products_imagecs", verbose_name="تصویر")
    price = models.IntegerField(verbose_name="قیمت")
    off = models.IntegerField(default=0, blank=True, verbose_name='درصد تخفیف')
    color = models.ManyToManyField(Color, verbose_name="رنگ")
    category = models.ManyToManyField(Category, related_name="sexy_toys_related_name", verbose_name="کتگوری")
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL, related_name="brand_related_name", verbose_name="برند")
    size = models.CharField(max_length=30, verbose_name="سایز")
    about = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    inventory = models.CharField(max_length=15, choices=INVENTORY, default="Available", verbose_name="موجود")
    publish = models.CharField(max_length=15, choices=PUBLISHD, default="unpublished", verbose_name="وضعیت انتشار")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    hits = models.ManyToManyField(ViewCounter, blank=True, related_name='hits_related')
    review = models.ManyToManyField(ReviewModel, blank=True, related_name='review_related')
    real = models.IntegerField(blank=True, default=0)
    reason_for_return = models.TextField(verbose_name="دلیل قبول نشدن محصول", blank=True, help_text='اگر قرار است محصول را رد کنید، چند خطی در مورد دلیل آن بنویسید')
    object = MyManager()

    @property
    def title_short(self):
        return truncatechars(self.title, 30)

    def show_category(self):
        return ", ".join([cat.category_name for cat in self.category.return_truestatus()])

    def return_pic(self):
        return format_html("<img src={0} width=75px height=80px;>".format(self.photo.url))

    def created_short(self):
        return date_format(self.created, format='SHORT_DATE_FORMAT', use_l10n=True)

    def get_absolute_url(self):
        return reverse("account:products")

    def discounted_price(self):
        res = self.price - (self.price * (self.off / 100))
        return int(res)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created",)


class ProductImage(models.Model):
    product = models.ForeignKey(SexToys, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_detail_image")


class Feature(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='features', on_delete=models.CASCADE, limit_choices_to={'parent__isnull': True})
    feature_slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    product = models.ForeignKey(SexToys, related_name='product_features', on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, related_name='product_features', on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    product_feature_slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.value

