from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from main.models import Movie, Person
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .serializers import MovieSerializer, PersonSerializer


class TopMovies(APIView):
    """Top movies"""
    # permission_classes = (IsAuthenticated,)
    @method_decorator(cache_page(60))
    def get(self, request):
        serializer = MovieSerializer(Movie.objects.top_movies(), context={'request': request}, many=True)
        return Response(serializer.data)


class PersonViewSet(ModelViewSet):
    """A simple ViewSet for listing or retrieving movies"""
    # permission_classes = (IsAuthenticated,)
    queryset = Person.objects.all_with_prefetch_films()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']


class MovieViewSet(ModelViewSet):
    """A simple ViewSet for listing or retrieving movies"""
    # permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title', 'year', 'genre']
    search_fields = ['title', 'genre']
    ordering_fields = ['title', 'year']




