from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("/<listing_id>", views.listing_item, name="listing_item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<item_id>", views.remove_item, name="remove_item"),
    path("categories/<str:cat>/", views.category, name="category"),
    path("disable_listing/<listing_id>", views.disable_listing, name="disable_listing"),
    path("closed", views.closed_listings, name="closed_listings"),
    path("search_listing", views.search_listing, name="search_listing"),
    path("like/<pk>", views.like_comment, name="like_comment"),
    path("dislike/<pk>", views.dislike_comment, name="dislike_comment"),
]
