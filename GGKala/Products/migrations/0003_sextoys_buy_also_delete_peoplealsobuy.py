# Generated by Django 4.2.1 on 2023-09-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_peoplealsobuy_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='sextoys',
            name='buy_also',
            field=models.ManyToManyField(related_name='people_buy_also', to='Products.sextoys'),
        ),
        migrations.DeleteModel(
            name='PeopleAlsoBuy',
        ),
    ]
