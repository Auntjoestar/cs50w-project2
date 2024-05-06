from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("list/<int:id>", views.listing, name="listing"),
    path("offer/<int:id>", views.create_offer, name="create_offer"),
    path("makeComment/<int:id>", views.make_comment, name="make_comment"),
    path("closedAuction/<int:id>", views.close_auction, name="close_auction"),
    path("watchlisting/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("watchlisted/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlisted/", views.show_watchlist, name="show_watchlist"),
    path("removewatchlisted/", views.removeWatchlist_from_Watchlist, name="removeWatchlist_from_Watchlist"),
    path("categories/", views.show_categories, name="show_categories"),
    path("mylisting/", views.my_listing, name="my_listing")
]
