from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Category, User, Listing, Bid, Comment, Watchlist


def index(request):
    listings = Listing.objects.filter(is_active=True).annotate(
        max_bid = Max("bids__bid")
    )
    return render(request, "auctions/index.html", {
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


@login_required
def create_listing(request):
    if request.method == "POST":
        seller = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        url = request.POST["image_url"]
        category = Category.objects.get(pk=request.POST["category"])

        listing = Listing(seller=seller, title=title, description=description, price=price, image=url, category=category)
        listing.save()

        return redirect("show_listing", listing.id)

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def show_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids_count = listing.bids.count()
    if bids_count:
        price = listing.bids.last().bid
        max_bidder = listing.bids.last().bidder
    else:
        price = listing.price
        max_bidder = None
    
    return render(request, "auctions/show_listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "price": price,
        "bids": bids_count,
        "bidder": max_bidder
    })


@login_required
def place_bid(request, listing_id):
    if request.method != "POST":
        return redirect("index")

    listing = Listing.objects.get(pk=listing_id)
    max_bid = listing.bids.last()

    if max_bid:
        price = max_bid.bid
    else:
        price = listing.price

    try:
        bid = int(request.POST["bid"])
    except:
        messages.error(request, "Invalid Bid! Place a valid Bid.")
        return redirect("show_listing", listing.id)
        
    if bid <= price:
        messages.error(request, "Bid amount must be greater than the current price.")
        return redirect("show_listing", listing.id)

    add_bid = Bid(bidder = request.user, listing = listing, bid = bid)
    add_bid.save()

    messages.success(request, "Your bid was placed successfully.")
    return redirect("show_listing", listing.id)
    


@login_required
def close_listing(request):
    if request.method != "POST":
        return redirect("index")
    

    listing = Listing.objects.get(pk=request.POST["close_listing"])
    if listing.seller != request.user:
        return redirect("show_listing", listing.id)
    
    max_bid = listing.bids.last()
    if max_bid:
        listing.winner = max_bid.bidder
    else:
        listing.winner = None

    listing.is_active = False
    listing.save()
    return redirect("show_listing", listing.id)


@login_required
def my_winnings(request):
    listings = Listing.objects.filter(winner=request.user).annotate(
        max_bid = Max("bids__bid")
    )
    return render(request, "auctions/index.html", {
        "listings": listings,
        "winner": True
    })


@login_required
def my_listing(request):
    listings = Listing.objects.filter(seller=request.user).annotate(
        max_bid = Max("bids__bid")
    )
    return render(request, "auctions/index.html", {
        "listings": listings,
        "my_listing": True
    })


@login_required
def comments(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    commentator = request.user
    comment = request.POST["comment"]

    add_comment = Comment(commentator=commentator, listing=listing, comment=comment)
    add_comment.save()

    return redirect("show_listing", listing.id)


@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchlists__user=request.user).annotate(
        max_bid = Max("bids__bid")
    )

    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist": True
    })


@login_required
def add_watchlist(request):
    if request.method != "POST":
        return redirect("index")
    
    listing = Listing.objects.get(pk=request.POST["add_listing"])

    if Watchlist.objects.filter(
        user = request.user,
        listing = listing
    ).exists():
        messages.error(request, "Listing already in your Watchlist.")
        return redirect("show_listing", listing.id)
    
    watchlist = Watchlist(user=request.user, listing=listing)
    watchlist.save()
    
    # Below line also does the same thing as above
    # Watchlist.objects.create(user=request.user, listing=listing)

    messages.success(request, "Listing added to your watchlist.")
    return redirect("show_listing", listing.id)


@login_required
def remove_watchlist(request):
    if request.method != "POST":
        return redirect("index")
    
    listing = Listing.objects.get(pk=request.POST["remove_listing"])

    Watchlist.objects.filter(listing=listing, user=request.user).delete()
    return redirect("watchlist")


def categories(request):
    category = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": category
    })


def category_listing(request, category_id):
    category = Category.objects.get(pk=category_id)

    listings = Listing.objects.filter(category=category, is_active=True).annotate(
        max_bid = Max("bids__bid")
    )
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category
    })
