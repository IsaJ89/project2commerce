# Generated by Django 5.0.6 on 2024-06-19 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_category_listing_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.TextField(default='Image link missing', max_length=50),
        ),
    ]