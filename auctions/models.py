from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    id= models.AutoField(primary_key=True)
    category_name =  models.CharField(max_length=50)
    def __str__(self):
        return f"{self.category_name}"

class User(AbstractUser):
    pass

class Listings(models.Model):
    id= models.AutoField(primary_key=True)
    ByUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name="listing_user")
    CurrentUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name="buyed_user",blank=True,null = True)
    Listing_Name = models.CharField(max_length=150)
    Price = models.IntegerField()
    Date = models.DateTimeField(default=now)
    Details = models.CharField(max_length=600)
    nBids = models.IntegerField(default=0,null=True)
    Img = models.ImageField(null=True,blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="Category")
    def __str__(self):
        return "id:"+str(self.id)+"Name:"+self.Listing_Name+" Price: $"+str(self.Price)



class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    WatchUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name="watch_user")
    WatchList = models.ForeignKey(Listings, on_delete=models.CASCADE,related_name="watch_listing")
    Date = models.DateTimeField(default=now)

class Bid(models.Model):
    id= models.AutoField(primary_key=True)
    Price = models.IntegerField()
    BidUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bid_user")
    BidList = models.ForeignKey(Listings, on_delete=models.CASCADE,related_name="bid_listing")
    Date = models.DateTimeField(default=now)

class Comments(models.Model):
    id= models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE,related_name="com_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="com_user")
    com = models.CharField(max_length=400)
    date = models.DateTimeField(default=now)
    def __str__(self):
        return f" {self.user} {self.com}"
