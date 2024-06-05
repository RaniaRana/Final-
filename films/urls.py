from django.urls import path, include

from . views import homepage, film_detail, add_films, add_reviews, top25, bottom25,register_view, autocomplete_search, search_results,add_to_watchlist, watchlist_view,get_cities, trailer_view
app_name = "films"

urlpatterns = [
    path("", homepage, name="home"),
    path("film/<int:pk>/", film_detail, name="f_detail"),
    path("add_films", add_films, name="add_films"),
    path("add_reviews", add_reviews, name="add_reviews"),
    path("top25", top25, name="top25"),
    path("bottom25", bottom25, name="bottom25"),
    path('register/', register_view, name='register'),
    path('get_cities/', get_cities, name='get_cities'),
    path('autocomplete/', autocomplete_search, name='autocomplete_search'),
    path('search/', search_results, name='search_results'),
    path('add_to_watchlist/<int:film_id>/', add_to_watchlist, name='add_to_watchlist'),
    path("watchlist/", watchlist_view, name="watchlist"),
    path('trailer/<int:pk>/', trailer_view, name='trailer_view'),
]
