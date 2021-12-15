from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.fields.files import ImageField, ImageFieldFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import Category,Listings,Comments,User, Watchlist, Bid
from django.contrib.auth.decorators import login_required


def index(request): 
    return render(request, "auctions/index.html",{
        "ActiveBids":Listings.objects.all()
    })

@login_required(login_url='/login/')
def watchlist(request):
    user_id = request.user.pk
    user_obj = User.objects.get(pk=user_id)
    data = user_obj.watch_user.all()
    return render(request, "auctions/watchlist.html",{
        "watched":data
    })

@login_required(login_url='/login/')
def create_listing(request): 
    if request.method == "POST":
        price = int(request.POST["price"])
        if price > 0 and "Image" in request.FILES and "listingname" in request.POST and "details" in request.POST and "category" in request.POST:
            listingname = request.POST["listingname"]
            details = request.POST["details"] 
            img = request.FILES["Image"]
            category = request.POST["category"]
            mycategory = Category.objects.get(category_name=category) 
            user = request.user
            Lis = Listings.objects.create(Listing_Name = listingname,ByUser = user,Price = price,Details = details,Img = img,Category = mycategory)
            return render(request, "auctions/create.html",{
                "category":Category.objects.all()
            })
        else:
            return render(request, "auctions/create.html",{
                "category":Category.objects.all(),
                "msg":"Error, the value can't be empty"
            })
    else:
        return render(request, "auctions/create.html",{
            "category":Category.objects.all()
        })

@login_required(login_url='/login/')
def created_view(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    created = user.listing_user.all()
    return render(request, "auctions/created.html",{
        "created":created
        })

@login_required(login_url=reverse_lazy("login"))
def listing(request,Listing_id): 
    msgerror = None
    user = request.user
    List_obj = Listings.objects.get(id=Listing_id)
    if List_obj.com_listing:
        com = Comments.objects.filter(listing = List_obj)
    else:
        com = None
    
    if request.method == "POST":
        if request.POST.get('btnwatch'):
            try:
                delet = Watchlist.objects.filter(WatchList = List_obj).get(WatchUser = user)
                delet.delete()
            except:
                Watchlist.objects.create(WatchUser = user,WatchList = List_obj)
        if request.POST.get('bid'):
            bid = int(request.POST["bid"])
            if bid > int(List_obj.Price) :
                List_obj.nBids = int(List_obj.nBids)+1
                List_obj.save()
                List_obj.Price = bid
                List_obj.save()
                List_obj.CurrentUser = user
                List_obj.save()
                Bid.objects.create(Price=bid,BidUser=user,BidList=List_obj)
                msgerror=None
            else:
                msgerror=" Error, the bid´s price is too low "
        else:
            msgerror="For purch yo need fill the bid form"
        
        if request.POST.get("com"):
            coment= str(request.POST["com"])
            Comments.objects.create(listing=List_obj,user=user,com=coment)

    if user == List_obj.CurrentUser:
        return render(request, "auctions/listings.html",{
            "Listing":List_obj,
            "current":"Your bid is the current bid"
        }) 
    return render(request, "auctions/listings.html",{
        "Listing":List_obj,
        "comment":com,
        "msg" : msgerror
    }) 

@login_required(login_url='/login/')
def category(request):
    category = Category.objects.all()
    return render(request, "auctions/category.html",{
        "category":category
        })

@login_required(login_url='/login/')
def categories(request,categoryId):
    cat = Category.objects.get(id = categoryId)
    List_obj = Listings.objects.filter(Category=cat)
    return render(request, "auctions/categories.html",{
        "category":cat,
        "item":List_obj
        })

@login_required(login_url='/login/')
def urbids(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    bids = user.bid_user.all()
    return render(request, "auctions/urbids.html",{
        "bids":bids
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
