from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm, BidForm, CommentForm
from .models import User, Listing, Bid, Watchlist, Comment





def index(request):
    listings = Listing.objects.filter(status=True)
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
    # get listing instance
    listing = Listing.objects.get(pk=listing_id)
    
    # process bids
    bid_form = BidForm()
    bid = listing.bids.last() # get the most recent bid(which would also be the highest)associated with a listing
    if bid:
        highest_bid = bid.bid_value
        winner = bid.placed_by
        listing.current_price = highest_bid
    else:
        listing.current_price = listing.starting_bid
        winner = None

    # process comments
    comment_form = CommentForm()
    comments = listing.comments.all()
    check_for_comments = comments.exists()

    if request.method == "POST":
        # process bid_form returned via POST method
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_value = bid_form.cleaned_data['bid_value']

            if bid_value is not None:
                if bid: # check if the listing has bids associate with it
                    highest_bid = bid.bid_value
                    if bid_value < highest_bid:
                        return render(request, "auctions/view_listing.html",{
                            "listing": listing,
                            "message": "Sorry, bid must be higher than the current price of the item",
                            "bid_form": bid_form,
                            "comment_form": comment_form
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
                            "bid_form": bid_form,
                            "comment_form": comment_form
                        })
                    else:
                        new_bid_object = bid_form.save(commit=False)
                        new_bid_object.item = listing
                        new_bid_object.placed_by = request.user
                        new_bid_object.placed_on = now()
                        new_bid_object.save()
                        listing.current_price = new_bid_object.bid_value
                        return HttpResponseRedirect(reverse("view_listing", args=(listing.id,)))
        
        # process comment returned via POST method
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            
            if comment is not None:
                new_comment_object = comment_form.save(commit=False)
                new_comment_object.item = listing
                new_comment_object.made_by = request.user
                new_comment_object.made_on = now()
                new_comment_object.save()
                return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
    
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
        "check_for_comments": check_for_comments,
        "winner" : winner
    })


def watchlist(request):
    listing_ids = []
    watchlist = Watchlist.objects.filter(user=request.user)

    # get the listing ids of all the items in the watchlist
    for item in watchlist:
        listing = Listing.objects.get(item=item.item)
        listing_ids.append(listing.id)
    
    # using the zip function to combine the two iterables and turning it into a list of tuples
    watchlist_and_ids = list(zip(watchlist, listing_ids))
    return render(request, "auctions/watchlist.html", {
        "watchlist_and_ids": watchlist_and_ids
    })

def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        listing = Listing.objects.get(id=listing_id)  # this is a Listing instance
        listing_to_add = Watchlist.objects.filter(user=request.user, item=listing) # this is a QuerySet
        
        # if listing is not already added to the watchlist
        if not listing_to_add:
            new_watchlist_object = Watchlist()
            new_watchlist_object.item = listing
            new_watchlist_object.user = request.user
            new_watchlist_object.save()
            return HttpResponseRedirect(reverse("watchlist"))
        else:
            return render(request, "auctions/view_listing.html", {
                "message": "This listing has already been added to your watchlist",
                "listing": listing,
                "bid_form": bid_form 
            })


def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        bid_form = BidForm(request.POST)
        listing_to_delete = Watchlist.objects.filter(user=request.user, item=listing)
        if listing_to_delete:
            listing_to_delete.delete()
            return HttpResponseRedirect(reverse("watchlist"))
        
        # if the listing to be removed does not exist in the watchlist
        else:
            return render(request, "auctions/view_listing.html", {
                "listing": listing,
                "bid_form": bid_form,
                "message": "Item has not been added to your watchlist yet" 
            })
    

def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        bid = listing.bids.last()
        if bid:
            listing.current_price = bid.bid_value
            message = "Congratulations for having sold your item! We hope you enjoyed selling with us"
        else:
            listing.current_price = listing.starting_bid
            message = "Sorry for having to close the auction without any bids! We hope you " \
            "have a better experience next time!"
        listing.status = False
        listing.save()
        
        return render(request, "auctions/view_listing.html", {
            "listing": listing,
            "message": message
        })

def categories(request):
    categories_to_display = []
    for choices in Listing.category_choices:
        categories_to_display.append(choices[1])

    return render(request, "auctions/categories.html",{
        "categories_to_display": categories_to_display,
    })


def listings_under_category(request, category):
    category = category.lower()
    listings = Listing.objects.filter(category=category)
    listings_check = listings.exists()
    return render(request, "auctions/listings_under_category.html",{
        "listings": listings,
        "listings_check": listings_check,
    })
