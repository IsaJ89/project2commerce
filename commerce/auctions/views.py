from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm, BidForm
from .models import User, Listing, Bid, Watchlist





def index(request):
    listings = Listing.objects.all()
    for listing in listings:
        bids = listing.bids.all()
        if bids.exists():
            highest_bid = max(bid.bid_value for bid in bids)
            listing.current_price = highest_bid
        else:
            listing.current_price = listing.starting_bid
        
    return render(request, "auctions/index.html",{
        "listings": listings
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False) # commit=False prevents the data from being saved to the database immediately
            listing.created_by = request.user
            listing.created_date = now()
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
    'form': form
})

def view_listing(request, listing_id):
    bid_form = BidForm()
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.all() # get bids associated with the listing; bids is a QuerySet object
    if bids.exists():
            highest_bid = max(bid.bid_value for bid in bids)
            listing.current_price = highest_bid
    else:
        listing.current_price = listing.starting_bid

    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_value = bid_form.cleaned_data['bid_value']
        
            if bids.exists():# check if the listing has bids associate with it
                highest_bid = max(bid.bid_value for bid in bids)
                if bid_value < highest_bid:
                        return render(request, "auctions/view_listing.html",{
                            "listing": listing,
                            "message": "Sorry, bid must be higher than the current price of the item",
                            "bid_form": bid_form
                        })
                else:
                    new_bid_object = bid_form.save(commit=False)
                    new_bid_object.item = listing
                    new_bid_object.placed_by = request.user
                    new_bid_object.placed_on = now()
                    new_bid_object.save()
                    listing.current_price = new_bid_object.bid_value
                    return HttpResponseRedirect(reverse("view_listing", args=(listing.id,)))
                        
            else:
                # if no pre-exising bids, check if bid_value is lesser than starting_bid
                if bid_value < listing.starting_bid:
                    return render(request, "auctions/view_listing.html",{
                        "listing" : listing,
                        "message": "Sorry! Your bid must be higher than the starting bid",
                        "bid_form": bid_form
                    })
                else:
                    new_bid_object = bid_form.save(commit=False)
                    new_bid_object.item = listing
                    new_bid_object.placed_by = request.user
                    new_bid_object.placed_on = now()
                    new_bid_object.save()
                    listing.current_price = new_bid_object.bid_value
                    return HttpResponseRedirect(reverse("view_listing", args=(listing.id,)))
    
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "bid_form": bid_form
    })

def watchlist(request):
    listing_ids = []
    watchlist = Watchlist.objects.filter(user=request.user)

    # get the listing ids of all the items in the watchlist
    for item in watchlist:
        listing = Listing.objects.get(item_name=item.item)
        listing_ids.append(listing.id)
    
    # using the zip function to combine the two iterables
    watchlist_and_ids = zip(watchlist, listing_ids)
    return render(request, "auctions/watchlist.html", {
        "watchlist_and_ids": watchlist_and_ids
    })

def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        new_watchlist_object = Watchlist()
        new_watchlist_object.item = listing
        new_watchlist_object.user = request.user
        new_watchlist_object.save()
        return HttpResponseRedirect(reverse("watchlist"))
