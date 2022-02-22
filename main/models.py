from uuid import uuid4
from django.conf import settings
from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone


class PersonManager(models.Manager):
    def all_with_prefetch_films(self):
        qs = self.get_queryset()
        return qs.prefetch_related('actors')


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField(default=timezone.now)
    died = models.DateField(null=True, blank=True)
    objects = PersonManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        return self.name


def movie_dir_path_uuid(instance, filename):
    return "{}/{}.{}".format(instance.movie_id, uuid4(), filename.split('.')[-1])


class MoviePicture(models.Model):
    pict = models.ImageField(upload_to=movie_dir_path_uuid)
    upload_time = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_picture', on_delete=models.CASCADE)


class MovieManager(models.Manager):
    def all_persons(self):
        qs = self.get_queryset()
        qs = qs.prefetch_related('actor')
        return qs

    def all_persons_and_score(self):
        qs = self.all_persons()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs

    def top_movies(self, limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(vote__sum=Sum('vote__value'))
        qs = qs.exclude(vote__sum=None)
        qs = qs.order_by('-vote__sum')
        qs = qs[:limit]
        return qs


class Movie(models.Model):
    WITHOUT_RATING = 0
    RATED_WORLD = 1
    RATED_18Y = 2
    RATED_L = 3
    STATUS_RATING = ((WITHOUT_RATING, 'WR - Without rating'),
                     (RATED_WORLD, 'RW - World rated'),
                     (RATED_18Y, 'R18 - 18+ rated'),
                     (RATED_L, 'RL - Limit rated'))
    title = models.CharField('Название фильма', max_length=100)
    preview = models.TextField('Описание фильма', max_length=5000)
    year = models.PositiveIntegerField('Год выпуска', default=1998)
    runtime = models.PositiveIntegerField('Длительность', default=10)
    genre = models.CharField('Жанр фильма', null=True, max_length=100, db_index=True)
    rating = models.IntegerField('Рейтинг фильма', choices=STATUS_RATING, default=WITHOUT_RATING)
    actor = models.ForeignKey(to='Person', null=True, related_name='actors', on_delete=models.SET_NULL, blank=True) # director ... rel_n = directed
    objects = MovieManager()

    class Meta:
        ordering = ('year', 'title')
        verbose_name = 'Film'
        verbose_name_plural = 'Films'

    def __str__(self):
        return "{} ({})".format(self.title, self.year)

    @staticmethod
    def get(pk=None):
        from rest_framework.exceptions import ValidationError
        try:
            qs = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist as ex:
            raise ValidationError(ex)
        return qs


class Roles(models.Model):
    title = models.CharField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} {} {}".format(self.movie_id, self.person_id, self.title)

    class Meta:
        unique_together = ('movie', 'person', 'title')
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class VoteManager(models.Manager):
    def get_vote_or_blank(self, movie, user):
        try:
            return Vote.objects.get(movie=movie, user=user)
        except Vote.DoesNotExist:
            return Vote(movie=movie, user=user)


class Vote(models.Model):
    like = 1
    dislike = -1
    value_choice = ((like, '+'), (dislike, '-'))
    # value = models.BigAutoField(choices=value_choice, primary_key=True)   #for old version django 2+, chg migrations
    value = models.SmallAutoField(choices=value_choice, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_vote', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote_on = models.DateTimeField(auto_now=True)
    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'movie')
