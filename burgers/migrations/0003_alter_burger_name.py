# Generated by Django 4.1.7 on 2023-02-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burgers', '0002_burger_description_burger_price_alter_burger_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burger',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]