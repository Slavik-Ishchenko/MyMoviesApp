from django.urls import include, path
from rest_framework import routers
from . import views
from django.views.decorators.cache import cache_page

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet, basename='movies')
router.register(r'person', views.PersonViewSet, basename='person')

app_name = 'mymovieapi'
urlpatterns = [
    # path('', cache_page(60)(include(router.urls))),  # такой вид роута - вывод названия фильмов
    path('', include(router.urls)),
    path('movies/top', views.TopMovies.as_view(), name='TopMovies'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]