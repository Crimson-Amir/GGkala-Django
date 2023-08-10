from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.formats import date_format


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    special_user = models.DateTimeField(blank=True, default=timezone.now, verbose_name='کاربر ویژه')

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    is_special_user.boolean = True

    def data_joined_short(self):
        return date_format(self.date_joined, format='SHORT_DATE_FORMAT', use_l10n=True)

    def data_special_short(self):
        return date_format(self.special_user, format='SHORT_DATE_FORMAT', use_l10n=True)

    class Meta:
        ordering = ['-date_joined']


class ViewCounter(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آی پی کاربر')

    def __str__(self):
        return self.ip_address
