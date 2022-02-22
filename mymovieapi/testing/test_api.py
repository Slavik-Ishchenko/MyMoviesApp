from django.urls import reverse
from main.models import Movie
from rest_framework import status
from rest_framework.test import APITestCase

from mymovieapi.serializers import MovieSerializer


class MovieApiTestCase(APITestCase):
    """Test for API. GET list of movies. POST new movie"""

    def test_get_movies(self):
        movie_1 = Movie.objects.create(title='Saw 6', year=2009, genre='Horror',
                                       runtime=10, preview='Horror 6', rating=2)
        movie_2 = Movie.objects.create(title='Saw 7', year=2010, genre='Horror',
                                       runtime=10, preview='Horror 7', rating=2)
        url = reverse('mymovieapi:movies-list')
        response = self.client.get(url)
        serializer_data = MovieSerializer([movie_1, movie_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_post_movies(self):
        url = reverse('mymovieapi:movies-list')
        data = {
            'title': 'Saw 6',
            'year': 2009,
            'genre': 'Horror',
            'runtime': 10,
            'preview': 'Horror 6',
            'rating': 2
        }
        serializer_data = MovieSerializer(data).data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer_data, response.data)
