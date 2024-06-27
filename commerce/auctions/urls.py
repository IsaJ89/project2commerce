from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.view_listing, name="view_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("close<int:listing_id>", views.close_auction, name="close_auction"),
    path("categories", views.categories, name="categories"),
    path("listings_under_category/<str:category>", views.listings_under_category, name="listings_under_category"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)