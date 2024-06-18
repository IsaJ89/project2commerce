from django.contrib import admin
from .models import User, Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "created_by", "created_date", "initial_bid")

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)