from django.shortcuts import render
from filim_pro.models import *
from filim_user.models import movie_rating as film_user_movie_rating
from django.db.models import Avg, Count

# Create your views here.
def home(request):
    data_list = movie.objects.all().order_by('-unique_id')[:10]
    rating = film_user_movie_rating.objects.values('movie_id').annotate(rating_value=Avg('rating_scale', distinct=True))
    context = { 'data_list': data_list, 'rating': rating }
    return render(request, 'index.html', context)
