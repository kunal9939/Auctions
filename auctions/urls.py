from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("my_winnings", views.my_winnings, name="my_winnings"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("show_listing<int:listing_id>", views.show_listing, name="show_listing"),
    path("place_bid<int:listing_id>", views.place_bid, name="place_bid"),
    path("comments<int:listing_id>", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("categories", views.categories, name="categories"),
    path("category_listing<int:category_id>", views.category_listing, name="category_listing")
]
 