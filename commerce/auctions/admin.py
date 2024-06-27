from django.contrib import admin
from .models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "created_by", "created_date", "status", "description", "starting_bid", "image", "category")
    fields = ("id", "item", "created_by", "created_date", "status", "description", "starting_bid", "image", "category")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "placed_by", "bid_value", "placed_on")
    fields = ("id", "item", "placed_by", "bid_value", "placed_on")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "item" , "user")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("item", "comment", "made_by", "made_on")
    fields = ("item", "comment", "made_by", "made_on")



admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Comment, CommentAdmin)