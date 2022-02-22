from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import VoteForm, MoviePictureForm, MoviesForm, ActorForm
from .models import Movie, Vote, Person


def index(request):
    return render(request, 'main/index.html')


class CreateMovie(View):
    def get(self, request):
        form = MoviesForm()
        return render(request, 'main/add_new_movie.html', context={'form': form})

    def post(self, request):
        bound_form = MoviesForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('MovieList')
        return render(request, 'main/add_new_movie.html', context={'form': bound_form})


class CreateActor(View):
    def get(self, request):
        form = ActorForm()
        return render(request, 'main/add_new_actor.html', context={'form': form})

    def post(self, request):
        bound_form = ActorForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('CreateMovie')
        return render(request, 'main/add_new_actor.html', context={'form': bound_form})


def main_page(request):
    return render(request, 'main/main_page.html')


class MovieList(ListView):
    template_name = 'main/movies_list.html'
    model = Movie
    # paginate_by = 10


class TopMovies(ListView):
    template_name = 'main/top10movies.html'
    queryset = Movie.objects.top_movies(limit=10)

    def get_queryset(self):
        limit = 10
        qs = Movie.objects.top_movies(limit=limit)
        return qs


class MovieDetail(DetailView):
    queryset = Movie.objects.all_persons_and_score()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['picture_form'] = self.movie_picture_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_blank(movie=self.object, user=self.request.user)
            if vote.pk:
                vote_url_form = reverse('UpdateVote', kwargs={'movie_id': vote.movie.id, 'pk': vote.pk})
            else:
                vote_url_form = reverse('CreateVote', kwargs={'movie_id': self.object.id})
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_url_form'] = vote_url_form
        return ctx

    def movie_picture_form(self):
        if self.request.user.is_authenticated:
            return MoviePictureForm()
        return None


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_films()


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('user not found' 'log in')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class MoviePictureUpload(CreateView):
    form_class = MoviePictureForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('MovieDetail', kwargs={'pk': movie_id})
        return movie_detail_url
