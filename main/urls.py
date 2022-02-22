from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('home', views.index),
    path('movies/', views.MovieList.as_view(), name='MovieList'),
    path('movies/create/', views.CreateMovie.as_view(), name='CreateMovie'),
    path('movies/create/actor', views.CreateActor.as_view(), name='CreateActor'),
    path('movies/top/', views.TopMovies.as_view(), name='TopMovies'),
    path('movies/top/<int:pk>', views.TopMovies.as_view(), name='TopIntMovies'),
    path('movies/<int:pk>', views.MovieDetail.as_view(), name='MovieDetail'),
    path('person/<int:pk>', views.PersonDetail.as_view(), name='PersonDetail'),
    path('movies/<int:movie_id>/vote', views.CreateVote.as_view(), name='CreateVote'),
    path('movies/<int:movie_id>/vote/<int:pk>', views.UpdateVote.as_view(), name='UpdateVote'),
    path('movies/<int:movie_id>/picture/upload', views.MoviePictureUpload.as_view(), name='MoviePictureUpload'),
]
