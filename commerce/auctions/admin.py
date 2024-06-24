from django.contrib import admin
from .models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "created_by", "created_date", "description", "starting_bid", "image", "category")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "placed_by", "bid_value", "placed_on")


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)