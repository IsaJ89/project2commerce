# Generated by Django 5.0.6 on 2024-06-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_bid_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('Fashion', 'Fashion'), ('Electronics', 'Electronics'), ('Health', 'Health'), ('Toys', 'Toys'), ('Home', 'Home'), ('Jewelry', 'Jewelry'), ('Automobiles', 'Automobiles'), ('Luxury', 'Luxury')], default='Add category', max_length=50),
        ),
    ]