from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User,Auction,Comment,Bid,Watchlist,AuctionForm,CommentForm,BidForm


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html",{
        "auctions" : auctions
    })

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = int(form.cleaned_data["starting_bid"])
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            userId = int(request.POST["userId"])
            user = User.objects.get(pk=userId)
            auction = Auction(title=title,description=description,current_bid=starting_bid,
            image_url=image_url,category=category, creator=user)
            auction.save()
            bid = Bid(starting_bid = starting_bid, current_bid = starting_bid, auction=auction)
            bid.save()
            auctions = Auction.objects.all()
            return render(request, "auctions/index.html", {
                "auctions":auctions,
            })
    else:
        form = AuctionForm()
        return render(request, "auctions/create.html",{
            "categories" : Auction.CATEGORY_CHOICES, "form":form
        })

@login_required(login_url='/login')
def detail(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    comments = Comment.objects.filter(auction_id=auction_id)
    bid = Bid.objects.get(auction_id=auction_id)
    user = User.objects.get(username=request.user.get_username())
    comment_form = CommentForm()
    bid_form = BidForm()
    try:
        watchlist = Watchlist.objects.get(
            user_id = user.id, auction_id = auction_id
    )
    except:
        return render(request,"auctions/detail.html", {
            "auction":auction,
            "comments": comments,
            "bid" :bid,
            "comment_form" : comment_form,
            "bid_form" : bid_form,
    })       
    
    return render(request,"auctions/detail.html", {
        "auction":auction,
        "comments": comments,
        "bid" :bid,
        "watch" : watchlist,
        "comment_form" : comment_form,
        "bid_form" : bid_form,
    })

@login_required(login_url='/login')
def comment(request, auction_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            userId = request.POST["userId"]
            user = User.objects.get(pk=userId)
            auction = Auction.objects.get(pk=auction_id)
            comment = Comment(comment=comment, auction=auction, commenter=user)
            comment.save()
            return HttpResponseRedirect(reverse("detail", args=(auction_id,)))  

@login_required(login_url='/login')
def bid(request,auction_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = int(form.cleaned_data["bid"])
            userId = request.POST["userId"]
            user = User.objects.get(pk=userId)
            auction = Auction.objects.get(pk=auction_id)
            old_bid = Bid.objects.get(auction_id=auction_id)
            if new_bid > old_bid.current_bid :
                old_bid.current_bid = new_bid
                old_bid.number_of_bid += 1
                old_bid.bidder = user
                auction.current_bid = new_bid
                old_bid.save()
                auction.save()
            else : 
                messages.info(request, "The bid must be at least as large as the starting bid, and must be greater than current bid.")
            return HttpResponseRedirect(reverse("detail", args=(auction_id,)))  

@login_required(login_url='/login')
def close(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        bid = Bid.objects.get(auction_id=auction_id)
        auction.state = "close"
        auction.save()
        if bid.number_of_bid > 0 :
            bid.winner = bid.bidder
            bid.ending_bid = bid.current_bid
            bid.save()
        return HttpResponseRedirect(reverse("detail", args=(auction_id,)))

@login_required(login_url='/login')
def watch(request,user_id):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        auction = Auction.objects.get(pk=auction_id)
        user = User.objects.get(pk=user_id)
        if request.POST["mode"] == "add":
            watch = Watchlist(auction = auction, user = user)
            watch.save()
        else:
            watch = Watchlist.objects.get(auction_id=auction_id,user_id=user_id)
            watch.delete()           
        return HttpResponseRedirect(reverse("watch", args=(user_id,)))
    else:
        user = User.objects.get(pk=user_id)
        watchlists = Watchlist.objects.filter(user_id=user_id)
        auctions = Auction.objects.none()
        if watchlists :
            for watch in watchlists:
                auction = Auction.objects.filter(pk=watch.auction_id)
                auctions = auctions | auction
            return render(request,"auctions/watch.html",{"auctions" : auctions})
        else:
            messages.info(request, "No WishLists.")
            return render(request, "auctions/watch.html")

def category(request,category):
    categories = Auction.CATEGORY_CHOICES
    if category == "all" or category == "AL":
        auctions = Auction.objects.all()
    else :
        auctions = Auction.objects.filter(category=category)
    return render(request, "auctions/category.html",{
        "categories" : categories, "auctions": auctions
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
