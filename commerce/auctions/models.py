from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass

class Listing(models.Model):
    item_name = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_date = models.DateTimeField(default=now)
    description = models.TextField(max_length=300, default="Description missing")
    initial_bid = models.DecimalField(max_digits=10,decimal_places=2)
    photo = models.TextField(max_length=150, default="Image link missing")
    category = models.CharField(max_length=50, default="Category missing")

    def __str__(self):
        return f"{self.item_name} {self.created_by.username} {self.created_date} {self.initial_bid}"


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass


