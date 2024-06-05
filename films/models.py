from django.db import models
from django.conf import settings
from django.dispatch import receiver 
from django.db.models.signals import post_save

certs = [
    ("U", "U"),
    ("PG", "PG"),
    ("12a", "12a"),
    ("15", "15"),
    ("18", "18"),
]

class Film(models.Model):
    title = models.CharField(max_length=250)
    released = models.DateField(auto_now=False, auto_now_add=False)
    certificate = models.CharField(max_length=3, choices=certs)
    duration = models.DurationField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=250)
    director_pic = models.URLField(max_length=500, default="")
    overview = models.TextField(max_length=1000)
    poster = models.URLField(max_length=500)
    trailer = models.URLField(max_length=1500, default="",blank=True, null=True)
    avg_rating = models.FloatField(default=0.0)
    popularity = models.IntegerField(default=0, editable=False)
    def __str__(self):
        return self.title

    def update_average_rating(self):
        avg_rating=self.ratings.all().aggregate(models.Avg("rating")).get("rating__avg", 0.0)
        self.average_rating = avg_rating
        self.save()
    @property
    def average_rating(self):
        return self.ratings.all().aggregate(models.Avg("rating")).get("rating__avg", 0.0)
    
    @property
    def num_votes(self):
        return self.ratings.all().aggregate(models.Count("rating")).get("rating__count", 0.0)
    
    def update_popularity(self):
        comment_count = self.comments.count()
        rate_count = self.num_votes
        rating = int(self.average_rating * 10) if self.average_rating else 0
        total_interactions = comment_count + rate_count + rating
        self.popularity = total_interactions % 100
        self.save()

@receiver(post_save, sender='films.Comment') 
def update_film_popularity_on_new_comment(sender, instance, created, **kwargs):
        if created:
            instance.film.update_popularity()

@receiver(post_save, sender='films.Rating')  
def update_film_popularity_on_new_rating(sender, instance, created, **kwargs):
        if created:
            instance.film.update_popularity()

class Rating(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name = "ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.film} - {self.user}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'film')

    def __str__(self):
        return f"{self.user.username}'s watchlist: {self.film.title}"
    
class Star(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='stars')
    star_name = models.CharField(max_length=250)
    star_pic = models.URLField(max_length=500)

    def __str__(self):
        return self.star_name
    
class UserCountryCity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.country}, {self.city}"
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.film.title}"

