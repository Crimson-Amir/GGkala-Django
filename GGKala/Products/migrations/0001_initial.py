# Generated by Django 4.2.1 on 2023-09-17 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
        ('account', '0001_initial'),
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('feature_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('category', models.ForeignKey(limit_choices_to={'parent__isnull': True}, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='Category.category')),
            ],
        ),
        migrations.CreateModel(
            name='SexToys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=65, verbose_name='عنوان')),
                ('photo', models.ImageField(upload_to='products_imagecs', verbose_name='تصویر')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('off', models.IntegerField(blank=True, default=0, verbose_name='درصد تخفیف')),
                ('size', models.CharField(max_length=30, verbose_name='سایز')),
                ('about', models.TextField(verbose_name='توضیحات')),
                ('slug', models.SlugField(unique=True, verbose_name='اسلاگ')),
                ('inventory', models.CharField(choices=[('available', 'موجود'), ('unavailable', 'ناموجود')], default='Available', max_length=15, verbose_name='موجود')),
                ('publish', models.CharField(choices=[('published', 'منتشر شده'), ('unpublished', 'پیش نویس'), ('pending', 'درحال بررسی'), ('returned', 'برگشت داده شده')], default='unpublished', max_length=15, verbose_name='وضعیت انتشار')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('real', models.IntegerField(blank=True, default=0)),
                ('reason_for_return', models.TextField(blank=True, help_text='اگر قرار است محصول را رد کنید، چند خطی در مورد دلیل آن بنویسید', verbose_name='دلیل قبول نشدن محصول')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brand_related_name', to='Category.brand', verbose_name='برند')),
                ('category', models.ManyToManyField(related_name='sexy_toys_related_name', to='Category.category', verbose_name='کتگوری')),
                ('color', models.ManyToManyField(to='Category.color', verbose_name='رنگ')),
                ('hits', models.ManyToManyField(blank=True, related_name='hits_related', to='account.viewcounter')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publisher_Products', to=settings.AUTH_USER_MODEL, verbose_name='اضافه کننده')),
                ('review', models.ManyToManyField(blank=True, related_name='review_related', to='review.reviewmodel')),
            ],
            options={
                'ordering': ('-created',),
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_detail_image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.sextoys')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('product_feature_slug', models.SlugField(blank=True, null=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='Products.feature')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='Products.sextoys')),
            ],
        ),
    ]
