from rest_framework import serializers
from main.models import Movie, Person


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    year = serializers.IntegerField(min_value=0)

    class Meta:
        model = Movie
        fields = ['title', 'genre', 'preview', 'year', 'runtime', 'rating']


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='mymovieapi:person-detail')
    birthday = serializers.DateField()
    died = serializers.DateField(allow_null=True)

    class Meta:
        model = Person
        fields = '__all__'
