from django.db import models
from account.models import User
# from Products.models import SexToys
from django.template.defaultfilters import truncatechars
from django.utils.formats import date_format


class ReviewModel(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product_slug = models.SlugField(blank=True, null=True)
    comment_title = models.CharField(max_length=50, verbose_name="عنوان")
    comment_body = models.TextField(max_length=500, verbose_name="دیدگاه")
    rate = models.IntegerField(default=0, blank=True, verbose_name="امتیاز")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.id)

    @property
    def comment_short(self):
        return truncatechars(self.comment_body, 30)

    def created_short(self):
        return date_format(self.created_at, format='SHORT_DATE_FORMAT')
