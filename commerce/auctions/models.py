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
                        ('jewelry','Jewelry'),
                        ('automobiles','Automobiles'),
                        ('luxury', 'Luxury')
                        ]
    item_name = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_date = models.DateTimeField(default=now)
    description = models.TextField(max_length=300, default="Add description")
    starting_bid = models.DecimalField(max_digits=10,decimal_places=2)
    current_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    category = models.CharField(max_length=50, default="Add category", choices=category_choices, blank=True)

    def __str__(self):
        return f"{self.item_name}"


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids',null=True)
    placed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids",null=True)
    bid_value = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    placed_on = models.DateTimeField(default=now)

    def __str__(self):
        return f"Item: {self.item} Bid Value:{self.bid_value}"

class Comment(models.Model):
    pass

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="is_watched_by", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watches", null=True)

