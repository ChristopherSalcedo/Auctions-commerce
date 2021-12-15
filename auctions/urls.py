from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("created", views.created_view, name="created_list"),
    path("create", views.create_listing, name="create_listing"),
    path("bids", views.urbids, name="bids_user"),
    path("category", views.category, name="category_menu"),
    path("category/<int:categoryId>", views.categories, name="categories_item"),
    path("listing/<int:Listing_id>", views.listing, name="listing") 
    ]
