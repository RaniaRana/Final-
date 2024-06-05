from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count
import os, json
from datetime import timedelta
from django.http import HttpResponse
from django.contrib.auth.models import User
from random import randint
from django.contrib.auth.decorators import login_required

from .models import Film, Rating, Watchlist, Star, UserCountryCity, Comment
from .filters import FilmFilter

from django.http import JsonResponse

from django.contrib.auth import login, authenticate
from django.urls import reverse
from .forms import RegisterForm

from django.db.models import Q


from django.db.models import Window, F
from django.db.models.functions import Rank


module_dir = os.path.dirname(__file__)

def top25(request):
    films = Film.objects.annotate(avr=Avg("ratings__rating"), votes=Count("ratings__rating")).order_by("-avr")[0:25]
    watchlist = Watchlist.objects.filter(user=request.user).values_list('film_id', flat=True) if request.user.is_authenticated else []
    login_url = reverse('login')
    context = {"films": films, "watchlist": watchlist, "login_url": login_url}
    return render(request, "films/homepage1.html", context)

def bottom25(request):
    films = Film.objects.annotate(avr=Avg("ratings__rating")).order_by("avr")[0:25]
    watchlist = Watchlist.objects.filter(user=request.user).values_list('film_id', flat=True) if request.user.is_authenticated else []
    login_url = reverse('login')
    context = {"films": films, "watchlist": watchlist, "login_url": login_url}
    return render(request, "films/homepage1.html", context)

#def filter_films(request):
#    films = FilmFilter(request.GET, queryset=Film.objects.all())
#    context = {"films":films, "form":films.form}
#    return render(request, "films/films_qs.html", context)

def add_films(request):
    file_path = os.path.join(module_dir, 'imdb_top_films.json')
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    no_added = 0
    for film_data in data:
        dur = film_data["Runtime"]
        f_dur = timedelta(minutes=int(dur[:-4]))
        film, created = Film.objects.update_or_create(
            title=film_data["Series_Title"],
            defaults={
                'released': f"{film_data['Released_Year']}-01-01",
                'certificate': film_data["Certificate"],
                'duration': f_dur,
                'genre': film_data["Genre"],
                'director': film_data["Director"],
                'director_pic': film_data["Director_Pic"],
                'overview': film_data["Overview"],
                'poster': film_data["Poster_Link"],
                'trailer': film_data.get("Trailer", "")
            }
        )

        stars = [
            {'star_name': film_data.get("Star1"), 'star_pic': film_data.get("Star1_Pic")},
            {'star_name': film_data.get("Star2"), 'star_pic': film_data.get("Star2_Pic")},
            {'star_name': film_data.get("Star3"), 'star_pic': film_data.get("Star3_Pic")},
            {'star_name': film_data.get("Star4"), 'star_pic': film_data.get("Star4_Pic")}
        ]

        for star_data in stars:
            if star_data['star_name'] and star_data['star_pic']:
                Star.objects.update_or_create(
                    film=film,
                    star_name=star_data['star_name'],
                    defaults={'star_pic': star_data['star_pic']}
                )

        no_added += 1

    msg = f"Added {no_added} films and their stars to the database."
    return HttpResponse(msg, content_type="text/plain")

def add_rev(g_film, g_user, g_rating):
    obj, create = Rating.objects.get_or_create(
        film = get_object_or_404(Film, pk=g_film),
        user = get_object_or_404(User, pk=g_user),
        rating = g_rating
    )

def homepage(request):
    films = Film.objects.annotate(avr=Avg("ratings__rating")).order_by("-avr")[0:10]  # Order by descending average rating
    watchlist = Watchlist.objects.filter(user=request.user).values_list('film_id', flat=True) if request.user.is_authenticated else []
    login_url = reverse('login')
    context = {"films": films, "watchlist": watchlist, "login_url": login_url}
    return render(request, "films/homepage.html", context)

def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    film.update_popularity()  # Update the popularity every time the detail is viewed

    # Calculate rank using a window function
    all_films = Film.objects.all().order_by('-popularity')
    previous_popularity = None
    rank = 0
    real_rank = 0

    # Calculate rank manually
    for f in all_films:
        real_rank += 1
        if f.popularity != previous_popularity:
            rank = real_rank
        if f.pk == film.pk:
            film_rank = rank  # Save the rank when we find our film
        previous_popularity = f.popularity

    total_seconds = int(film.duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    duration = f"{hours}h {minutes}m"
    genres = film.genre.split(",")

    stars = film.stars.all()  # Fetch stars related to the film
    comments = film.comments.all().order_by('created_at')  # Fetch all comments ordered by creation date

    context = {
        "film": film,
        "genres": genres,
        "dura": duration,
        "trailer": film.trailer,
        "stars": stars,
        "comments": comments,  # Include comments in the context
        "rank": film_rank,  # Include rank in the context
    }

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('films:login')
        if 'rating' in request.POST:
            obj = Rating.objects.update_or_create(
                film = get_object_or_404(Film, pk=request.POST["film"]),
                user = get_object_or_404(User, pk=request.user.id),
                rating = request.POST["rating"]
            )
            rated = Rating.objects.get(film=request.POST["film"], user=request.user)
            context["rating"] = rated
            return render(request, 'films/partials/user_review.html', context)
        if 'comment' in request.POST:
            comment_content = request.POST.get("comment")
            Comment.objects.create(user=request.user, film=film, content=comment_content)
            return redirect('films:f_detail', pk=pk)  # Redirect to refresh the page and show the new comment

    if request.user.is_authenticated:
        rating = Rating.objects.filter(user=request.user, film=film).first()
    else:
        rating = None
    context["rating"] = rating  # Ensure rating is always in context

    return render(request, "films/f_detail.html", context)

def add_reviews(request):
    for j in range(0,1000):
        for i in range(2,6):
            filmID = randint(451, 525)
            filmRating = randint(1,10)
            add_rev(filmID, i, filmRating)
    return redirect("films:home")

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'countries.json')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['surname']
            user.save()
            
            country = request.POST.get('country')
            city = request.POST.get('city')

            UserCountryCity.objects.create(user=user, country=country, city=city)
            
            # Specify the authentication backend
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("films:home")
        else:
            print(form.errors)  # Debugging line to print form errors to console
    else:
        form = RegisterForm()

    with open(file_path, "r", encoding="utf-8") as f:
        countries = json.load(f).keys()
    
    return render(request, 'registration/register.html', {'form': form, 'countries': countries})

def get_cities(request):
    country = request.GET.get('country')
    if country:
        with open(file_path, "r", encoding="utf-8") as f:
            countries = json.load(f)
            cities = countries.get(country, [])
            return JsonResponse({'cities': cities})
    return JsonResponse({'cities': []})
"""
def autocomplete_search(request):
    term = request.GET.get('term', '')
    category = request.GET.get('category', 'all')
    
    if term:
        if category == 'title':
            qs = Film.objects.filter(title__icontains=term)
        elif category == 'director':
            qs = Film.objects.filter(director__icontains=term)
        elif category == 'star1':
            qs = Film.objects.filter(star1__icontains=term)
        elif category == 'star2':
            qs = Film.objects.filter(star2__icontains=term)
        elif category == 'star3':
            qs = Film.objects.filter(star3__icontains=term)
        else:  # 'all'
            qs = Film.objects.filter(
                Q(title__icontains=term) |
                Q(director__icontains=term) |
                Q(star1__icontains=term) |
                Q(star2__icontains=term) |
                Q(star3__icontains=term)
            )
        results = qs.values('title', 'director', 'genre', 'poster', 'star1', 'star2', 'star3')
        return JsonResponse(list(results), safe=False)
    return JsonResponse([], safe=False)
"""
def autocomplete_search(request):
    term = request.GET.get('term', '')
    category = request.GET.get('category', 'all')

    if term:
        if category == 'title':
            qs = Film.objects.filter(title__icontains=term)
        elif category == 'director':
            qs = Film.objects.filter(director__icontains=term)
        elif category == 'stars':
            # Search for stars and include related film information
            qs = Star.objects.filter(star_name__icontains=term).select_related('film')
        else:  # 'all'
            qs = Film.objects.filter(
                Q(title__icontains=term) |
                Q(director__icontains=term) |
                Q(stars__star_name__icontains=term)
            ).distinct()
        
        results = [
            {
                'title': film.title,
                'director': film.director,
                'poster': film.poster,
                'stars': [star.star_name for star in film.stars.all()],
            } for film in qs
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)





def search_results(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')
    context = {"query": query, "category": category}

    if query:
        if category == 'title':
            title_results = Film.objects.filter(title__icontains=query)
            context["title_results"] = title_results
        elif category == 'director':
            director_results = Film.objects.filter(director__icontains=query)
            context["director_results"] = director_results
        elif category == 'stars':
            star_results = Star.objects.filter(star_name__icontains=query).select_related('film')
            context["star_results"] = star_results
        else:  # 'all'
            title_results = Film.objects.filter(title__icontains=query)
            director_results = Film.objects.filter(director__icontains=query)
            star_results = Star.objects.filter(star_name__icontains=query).select_related('film')
            
            context.update({
                "title_results": title_results,
                "director_results": director_results,
                "star_results": star_results,
            })

    return render(request, "films/search_results.html", context)


def trailer_view(request, pk):
    film = get_object_or_404(Film, pk=pk)
    context = {
        "film": film,
        "trailer_url": film.trailer  # Make sure your Film model includes a 'trailer' field
    }
    return render(request, "films/trailer.html", context)


@login_required
def add_to_watchlist(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user, film=film)
    if created:
        return JsonResponse({'status': 'added'})
    else:
        return JsonResponse({'status': 'exists'})
    
@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('film')
    context = {
        "watchlist_items": watchlist_items,
    }
    return render(request, "films/watchlist.html", context)