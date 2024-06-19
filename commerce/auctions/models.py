from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass

class Listing(models.Model):
    category_choices = [('fashion','Fashion'),
                        ('electronics','Electronics'),
                        ('health','Health'),
                        ('toys','Toys'),
                        ('home','Home'),
                        ('jewelry','Jewelry')
                        ]
    item_name = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_date = models.DateTimeField(default=now)
    description = models.TextField(max_length=300, default="Add description")
    initial_bid = models.DecimalField(max_digits=10,decimal_places=2)
    photo = models.URLField(max_length=50, blank=True)
    category = models.CharField(max_length=50, default="Add category", choices=category_choices, blank=True)



class Bid(models.Model):
    pass

class Comment(models.Model):
    pass


