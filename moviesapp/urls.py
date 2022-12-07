from django.urls import path
from . import views

urlpatterns = [
    path('path', views.home_1, name="home"),
    path('movie-finder-id', views.movieFinderByID, name='movieFinderByID'),
    path('movie-detail', views.movieDetail, name='movieDetail'),
    path('cast-actor-profile', views.CastActorProfile, name='CastActorProfile'),
    path('years-genre-language', views.movieDetailsByYearsOrGenresOrLanguagesOrAll, name='yearsGenreLanguage'),
    path('rated-movie-users', views.ratedMovieByUsers, name='ratedMovieByUsers'),
    path('test-data', views.testData, name='testData'),
    path('top-rated', views.topRated, name='topRated')

]
