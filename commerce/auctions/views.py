from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Auction, Watchlist, Bid, Comment, Image
from .forms import AuctionForm, CommentForm, BidForm, ImageForm
from django.contrib import messages
import datetime
from django.core.paginator import Paginator


def index(request):
    listings = Auction.objects.all()
    listings = listings.filter(active = True)
    listings = listings.order_by("-date_created").all()

    # Set up Paginaton
    p = Paginator(listings, 10)
    page = request.GET.get("page")
    listings = p.get_page(page)

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def closed_listings(request):
    listings = Auction.objects.all()
    listings = listings.filter(active = False)
    listings = listings.order_by("-date_created").all()
    return render(request, "auctions/closed_listings.html", {
        "listings": listings
    })


# Create listing
def create_listing(request):
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        if form.is_valid():
            listing = form.save(commit=False)
            listing.product_owner = request.user
            listing.save()
            for i in files:
                Image.objects.create(auction=listing, image=i)

            return HttpResponseRedirect(reverse ('auctions:index'))
    else:
        form = AuctionForm()
        imageform = ImageForm()

    return render(request, "auctions/create_listing.html", {
        "form": form,
        "imageform": imageform,
    })



def listing_item(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    comments = listing.comments.all()
    total_comment_likes = ""
    total_comment_dislikes = ""
    for comment in comments:
        total_comment_likes = comment.total_likes()
        total_comment_dislikes = comment.total_dislikes()
    auction_user = request.user.id
    watchlist_ids = []
    watchlist_all = Watchlist.objects.filter(watchlist_user=auction_user)
    for item in watchlist_all:
        watchlist_ids.append(item.watchlist_item.id)

    if 'add_comment' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = Auction.objects.get(pk=listing.id)
            comment.name = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id == "":
                comment.save()
            else:
                comment.parent = Comment.objects.get(id=parent_id)
                comment.save()

            return HttpResponseRedirect(reverse ('auctions:listing_item', args=(str(listing_id),)))

    elif 'add_bid' in request.POST:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            if listing.highest_bid:
                current_bid = listing.highest_bid
            else:
                current_bid = listing.starting_bid

            bid = bid_form.save(commit=False)
            bid.auction_biding = Auction.objects.get(pk=listing.id)
            bid.bidder = request.user
            bid.new_bid = bid_form['new_bid'].value()
            if int(bid.new_bid) > int(current_bid):
                bid.save()
                listing.highest_bid = bid.new_bid
                listing.save()
                messages.success(request, ("Your Bid Is Currently The Highest Bid"))

            else:
                messages.success(request, ("Your Bid Is Not Big Enough"))

            return HttpResponseRedirect(reverse ('auctions:listing_item', args=(str(listing_id),)))

    else:
        form = CommentForm()
        bid_form = BidForm()

    return render(request, "auctions/listing_item.html", {
        "listing": listing,

        "form": form,
        "bid_form": bid_form,
        "watchlist_all": watchlist_all,
        "watchlist_ids": watchlist_ids,
        "auction_user": auction_user,
        "total_comment_likes": total_comment_likes,
        "total_comment_dislikes": total_comment_dislikes,
    })


# Like comments
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    listing_id = comment.product.id
    return HttpResponseRedirect(reverse ('auctions:listing_item', args=(str(listing_id),)))


# Dislike comments
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.dislikes.add(request.user)
    listing_id = comment.product.id
    return HttpResponseRedirect(reverse ('auctions:listing_item', args=(str(listing_id),)))


# Add item to a watchlist
def watchlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            me = request.user.id
            auction_user = User.objects.get(pk=me)
            product = int(request.POST.get("watchlist_product", False))
            auction_product = Auction.objects.get(pk=product)
            watchlist_item = Watchlist.objects.create(watchlist_user=auction_user, watchlist_item=auction_product)
            watchlist_item.save()
            watchlist_all = Watchlist.objects.filter(watchlist_user=auction_user)
            return HttpResponseRedirect(reverse ('auctions:watchlist'))

    else:
        if request.user.is_authenticated:
            auction_user = request.user.id
            watchlist_all = Watchlist.objects.filter(watchlist_user=auction_user, watchlist_item__active = True)
            return render(request, 'auctions/watchlist.html', {
                "watchlist_all": watchlist_all,
                "message": "Your Watchlist Is Empty",
            })

    return render(request, 'auctions/watchlist.html', {
        "watchlist_all": watchlist_all,
    })


# Remove item from a watchlist
def remove_item(request, item_id):
    auction_item = Auction.objects.get(pk=item_id)
    if request.user.is_authenticated:
        watchlist_remove = Watchlist.objects.filter(watchlist_item = auction_item)
        watchlist_remove.delete()
        messages.success(request, ("Item Removed!"))
        return redirect('auctions:watchlist')
    else:
        messages.success(request, ("You aren't Authorized To Remove This Item!"))
        return redirect('auctions:watchlist')



# Disable listing
def disable_listing(request, listing_id):
    auction_item = Auction.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        auction_item.active = False
        auction_item.date_closed = datetime.datetime.now()
        auction_item.save()
        messages.success(request, ("Listing Deactivated!"))
        return HttpResponseRedirect(reverse ('auctions:listing_item', args=listing_id))
    else:
        messages.success(request, ("You aren't Authorized To Remove This Item!"))


def categories_list(request):
    pass


"""
# List all the categories
def categories_list(request):
    categories = []
    all_categories = Auction.CATEGORY_CHOICES
    for category in all_categories:
        categories.append(category[0])
    return {
        "categories": categories
    }
"""


def category(request, cat):
    category_list = Auction.objects.filter(product_category=cat)
    category_list = category_list.order_by("-date_created").all()
    return render(request, "auctions/category.html", {
        "cat": cat,
        "category_list": category_list,
    })


def search_listing(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched_item = Auction.objects.filter(product_name__contains=searched)
        searched_item = searched_item.order_by("-date_created").all()
        return render(request, "auctions/search_listing.html", {
            "searched": searched,
            "searched_item": searched_item,
        })

    else:
        return render(request, 'auctions/search_listing.html', {})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
