# Generated by Django 5.0.6 on 2024-06-26 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_alter_bid_bid_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
