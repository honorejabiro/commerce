from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Listing, User, Category, Comment, Bid
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html",{
        "listings":listings
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


def new_listing(request):
    user = request.user
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        bid = int(request.POST['Bid'])
        bid1 = Bid.objects.create(user=user, price=bid)
        description = request.POST['Description']
        url = request.POST['urlimage']
        category1 = request.POST['category']
        category = Category.objects.get(id=category1)
        owner = user
        listing = Listing.objects.create(title=title, price=bid1, owner=owner, description=description,image=url, category=category)    
    if user.is_authenticated:
        return render(request, 'auctions/create_listing.html',{
            'categories':categories
        })
    else:
        return redirect('login')
    
def listing(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    isOwner = listing.owner.username == request.user.username
    if listing in user.watchlist.all():
        check = True
    else:
        check = False
    return render(request, "auctions/listing.html", {
        "listing":listing, "check":check,
        "isOwner":isOwner
    })

def watchlist(request):
    user = request.user
    watchlists = user.watchlist.all()
    return render(request, 'auctions/watchlist.html',{
        "watchlists":watchlists, "user":user
    })

def watchlist_manager(request, id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=id)
        user = request.user
        if request.POST['position'] == 'member':
            user.watchlist.remove(listing)
            watchlists = user.watchlist.all()
            return render(request, 'auctions/watchlists.html',{
                "watchlists":watchlists, "user":user
            })
        else:
            user.watchlist.add(listing)
            watchlists = user.watchlist.all()
            return render(request, 'auctions/watchlists.html',{
                "watchlists":watchlists, "user":user
            })
    
def watchlist_page(request, user_id):
    user = User.objects.get(id=user_id)
    listings = user.watchlist.all()
    return render(request, 'auctions/watchlist_page.html', {
        'listings':listings, 'user':user
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories':categories
    })

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category.html',{
        'listings':listings, 'category':category
    })

@login_required
def bid(request, id):
    user = request.user
    listing = Listing.objects.get(id=id)
    price = request
    

@login_required
def comment(request, id):
    if request.method == 'POST':
        user = request.user
        listing = Listing.objects.get(id=id)
        message = request.POST['message']
        comment = Comment(user=user, listing=listing, message=message)
        comment.save()
        comments = Comment.objects.filter(listing=listing)
        if listing in user.watchlist.all():
            check = True
        else:
            check = False
        return render(request, "auctions/listing.html", {
            "listing":listing, "check":check, 'comments':comments
        })

@login_required
def bid(request, id):
    user = request.user
    price = int(request.POST['bid'])
    listing = Listing.objects.get(id=id)
    original_bid = listing.price.price
    if original_bid < price:
        bid = Bid.objects.create(user=user,price=price)
        listing.price = bid
        listing.save()
        if listing in user.watchlist.all():
            check = True
        else:
            check = False
        return render(request, "auctions/listing.html", {
            "listing":listing, "check":check, "updated":True, "message":"Bid applied successfully"
        })

    else:
        if listing in user.watchlist.all():
            check = True
        else:
            check = False
        return render(request, "auctions/listing.html", {
            "listing":listing, "check":check, "updated":False, "message":"Sorry, but the bid is low."
        })
    
def close(request, id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=id)
        user = request.user
        if listing in user.watchlist.all():
            check = True
        else:
            check = False
        listing.isActive = False
        listing.save()
        return render(request, 'auctions/listing.html',{
            "message":"Listing successfully closed",
            "check":check,
            "listing":listing,
            "updated":True
        })

    