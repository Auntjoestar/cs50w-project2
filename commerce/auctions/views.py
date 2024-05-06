from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Comments, Winners, Listing, Offers

LOGIN_URL = "login"


def index(request):
    active_listing = Listing.objects.filter(active=True).order_by("-created_at")
    user = request.user
    choices = []
    message = "Welcome to the #1 site of dnd's auctions"
    for i in Listing.CATEGORY_CHOICES:
        choices.append(i[1])
    if user.is_authenticated:
        watched_listing = user.listingWatchlist.all()
        return render(
            request,
            "auctions/index.html",
            {
                "listing": active_listing,
                "watchlist": watched_listing,
                "choices": choices,
                "message": message,
            },
        )
    return render(
        request,
        "auctions/index.html",
        {
            "listing": active_listing,
            "choices": choices,
        },
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        choices = []
        for i in Listing.CATEGORY_CHOICES:
            choices.append(i[1])
        return render(request, "auctions/login.html", {"choices": choices})


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

        if not username:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username must be provided."},
            )
        if not email:
            return render(
                request, "auctions/register.html", {"message": "Email must be provied."}
            )
        if not password:
            return render(
                request,
                "auctions/register.html",
                {"message": "Passwords must be provided."},
            )
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        choices = []
        for i in Listing.CATEGORY_CHOICES:
            choices.append(i[1])
        return render(
            request,
            "auctions/register.html",
            {
                "choices": choices,
            },
        )


@login_required
def create_listing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        img = request.POST["img"]
        category = request.POST["category"]
        price = request.POST["price"]
        choices = []
        for i in Listing.CATEGORY_CHOICES:
            choices.append(i[1])
        if not title:
            if user.is_authenticated:
                watched_listing = user.listingWatchlist.all()
            return render(
                request,
                "auctions/create.html",
                {
                    "choices": choices,
                    "message": "Title must be provided.",
                    "watchlist": watched_listing,
                },
            )
        if not description:
            if user.is_authenticated:
                watched_listing = user.listingWatchlist.all()
            return render(
                request,
                "auctions/create.html",
                {
                    "choices": choices,
                    "message": "Description must be provided.",
                    "watchlist": watched_listing,
                },
            )
        if not price:
            if user.is_authenticated:
                watched_listing = user.listingWatchlist.all()
                return render(
                    request,
                    "auctions/create.html",
                    {
                        "choices": choices,
                        "message": "Price must be provided.",
                        "watchlist": watched_listing,
                    },
                )
        offer = Offers(offerer=user, offer_amount=price)
        offer.save()
        listing = Listing(
            lister=user,
            title=title,
            description=description,
            imageLink=img,
            categories=category,
            price=offer,
        )
        listing.save()
        choices = []
        watched_listing = request.user.listingWatchlist.all()
        return HttpResponseRedirect(reverse("listing", kwargs={"id": listing.id}))
    else:
        choices = []
        watched_listing = request.user.listingWatchlist.all()
        for i in Listing.CATEGORY_CHOICES:
            choices.append(i[1])
        return render(
            request,
            "auctions/create.html",
            {"choices": choices, "watchlist": watched_listing},
        )


def listing(request, id):
    try:
        listing = Listing.objects.get(pk=id)
    except:
        return HttpResponse("ERROR 404")
    if request.user.is_authenticated:
        isInWatchList = request.user in listing.watchlist.all()
    else:
        isInWatchList = False
    comments = Comments.objects.filter(product=listing)
    isLister = request.user == listing.lister
    if request.user.is_authenticated:
        watched_listing = request.user.listingWatchlist.all()
    else:
        watched_listing = None
    Winner = None
    isWinner = False
    if listing.active is False:
        Winner = Winners.objects.get(item=listing)
        if Winner.winned_by == request.user:
            isWinner = True
    choices = []
    for i in Listing.CATEGORY_CHOICES:
        choices.append(i[1])
    return render(
        request,
        "auctions/list.html",
        {
            "listing": listing,
            "isInWatchList": isInWatchList,
            "comments": comments,
            "winner": Winner,
            "isLister": isLister,
            "isWinner": isWinner,
            "watchlist": watched_listing,
            "choices": choices,
        },
    )


@login_required
def create_offer(request, id):
    listing = Listing.objects.get(pk=id)
    isInWatchList = request.user in listing.watchlist.all()
    watched_listing = request.user.listingWatchlist.all()
    comments = Comments.objects.filter(product=listing)
    isLister = request.user == listing.lister
    Winner = None
    isWinner = False
    choices = []
    for i in Listing.CATEGORY_CHOICES:
        choices.append(i[1])
    if listing.active is False:
        Winner = Winners.objects.get(item=listing)
        if Winner.winned_by == request.user:
            isWinner = True
    offerer = request.user
    offer = request.POST["bid"]
    if not offer:
        return render(
            request,
            "auctions/list.html",
            {
                "message": "Offer must be provided.",
                "listing": listing,
                "isInWatchList": isInWatchList,
                "watchlist": watched_listing,
                "comments": comments,
                "winner": Winner,
                "isLister": isLister,
                "isWinner": isWinner,
                "choices": choices,
            },
        )
    if int(offer) > listing.price.offer_amount:
        updatedOffer = Offers(offerer=offerer, offer_amount=int(offer))
        updatedOffer.save()
        listing.price = updatedOffer
        listing.save()
        return render(
            request,
            "auctions/list.html",
            {
                "update": True,
                "message": "Offer succesfully raised.",
                "listing": listing,
                "isInWatchList": isInWatchList,
                "watchlist": watched_listing,
                "comments": comments,
                "winner": Winner,
                "isLister": isLister,
                "isWinner": isWinner,
                "choices": choices,
            },
        )
    else:
        choices = []
        for i in Listing.CATEGORY_CHOICES:
            choices.append(i[1])
        return render(
            request,
            "auctions/list.html",
            {
                "update": False,
                "message": "Offer has to be greater than current price.",
                "listing": listing,
                "isInWatchList": isInWatchList,
                "watchlist": watched_listing,
                "comments": comments,
                "winner": Winner,
                "isLister": isLister,
                "isWinner": isWinner,
                "choices": choices,
            },
        )


@login_required
def make_comment(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    comment = request.POST.get("comment")
    isInWatchList = request.user in listing.watchlist.all()
    watched_listing = request.user.listingWatchlist.all()
    comments = Comments.objects.filter(product=listing).order_by("-commented_at")
    isLister = request.user == listing.lister
    Winner = None
    isWinner = False
    if listing.active is False:
        Winner = Winners.objects.get(item=listing)
        if Winner.winned_by == request.user:
            isWinner = True
    if not comment:
        return render(
            request,
            "auctions/list.html",
            {
                "update": False,
                "message": "Comment must be provided.",
                "listing": listing,
                "isInWatchList": isInWatchList,
                "watchlist": watched_listing,
                "comments": comments,
                "winner": Winner,
                "isLister": isLister,
                "isWinner": isWinner,
            },
        )
    newComment = Comments(user=user, product=listing, comment=comment)
    newComment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing.id}))


@login_required
def close_auction(request, id):
    close = request.POST["closed"]
    if close:
        listing = Listing.objects.get(pk=id)
        listing.active = False
        listing.save()
        iswinner = listing.price.offerer
        winner = Winners(item=listing, winned_by=iswinner)
        winner.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"id": listing.id}))


@login_required
def addWatchlist(request, id):
    add = request.POST["add"]
    if add:
        user = request.user
        listing = Listing.objects.get(pk=id)
        listing.watchlist.add(user)
        return HttpResponseRedirect(reverse("listing", kwargs={"id": listing.id}))


@login_required
def removeWatchlist(request, id):
    remove = request.POST["remove"]
    if remove:
        user = request.user
        listing = Listing.objects.get(pk=id)
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("listing", kwargs={"id": listing.id}))


@login_required
def removeWatchlist_from_Watchlist(request):
    remove = request.POST["remove"]
    id = request.POST["id"]
    if remove:
        user = request.user
        listing = Listing.objects.get(pk=id)
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("show_watchlist"))


@login_required
def show_watchlist(request):
    user = request.user
    listing = user.listingWatchlist.all()
    watched_listing = request.user.listingWatchlist.all()
    choices = []
    for i in Listing.CATEGORY_CHOICES:
        choices.append(i[1])
    return render(
        request,
        "auctions/watchlist.html",
        {"listing": listing, "watchlist": watched_listing, "choices": choices},
    )


def show_categories(request):
    category = request.GET.get("category")
    active_listing = Listing.objects.filter(active=True, categories=category).order_by(
        "-created_at"
    )
    user = request.user
    choices = []
    for i in Listing.CATEGORY_CHOICES:
        choices.append(i[1])
    if user.is_authenticated:
        watched_listing = user.listingWatchlist.all()
        return render(
            request,
            "auctions/index.html",
            {
                "listing": active_listing,
                "watchlist": watched_listing,
                "choices": choices,
            },
        )
    return render(
        request, "auctions/index.html", {"listing": active_listing, "choices": choices}
    )


def my_listing(request):
    user = request.user
    active_listing = Listing.objects.filter(active=True, lister=user).order_by(
        "-created_at"
    )
    choices = []
    for i in Listing.CATEGORY_CHOICES:
        choices.append(i[1])
    if user.is_authenticated:
        watched_listing = user.listingWatchlist.all()
        return render(
            request,
            "auctions/index.html",
            {
                "listing": active_listing,
                "watchlist": watched_listing,
                "choices": choices,
            },
        )
    return render(
        request, "auctions/index.html", {"listing": active_listing, "choices": choices}
    )
