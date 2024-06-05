import django_filters
from .models import Film

class FilmFilter(django_filters.FilterSet):
    avg_rating = django_filters.RangeFilter(field_name="avg_rating")
    
    class meta:
      model = Film
      fields = {
          "title":["icontains"], 
                  "certificate":["exact"],
                    }