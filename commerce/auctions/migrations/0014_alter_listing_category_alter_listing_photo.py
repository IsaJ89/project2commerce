# Generated by Django 5.0.6 on 2024-06-19 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_listing_category_alter_listing_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('select', 'Select'), ('fashion', 'Fashion'), ('electronics', 'Electronics'), ('health', 'Health'), ('toys', 'Toys'), ('home', 'Home'), ('jewelry', 'Jewelry')], default='Add category', max_length=50),
        ),
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.URLField(blank=True, default="Add a link to your product's image", max_length=50),
        ),
    ]