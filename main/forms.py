from django import forms
from django.contrib.auth import get_user_model
from .models import Vote, Movie, MoviePicture, Person
from django.forms import ModelForm, TextInput, DateInput


class VoteForm(ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=get_user_model().objects.all(), disabled=True, )
    movie = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Movie.objects.all(), disabled=True, )
    value = forms.ChoiceField(label='Vote', widget=forms.RadioSelect, choices=Vote.value_choice)

    class Meta:
        model = Vote
        fields = ('value', 'user', 'movie')


class MoviePictureForm(ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=get_user_model().objects.all(), disabled=True, )
    movie = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Movie.objects.all(), disabled=True, )

    class Meta:
        model = MoviePicture
        fields = ('pict', 'user', 'movie')


class ActorForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {'name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}),
                   'birthday': DateInput(format='%d-%m-%Y', attrs={'class': 'form-control',
                                                                   'placeholder': 'Дата рождения (ГГГГ-ММ-ДД)'}),
                   'died': DateInput(format='%d-%m-%Y', attrs={'class': 'form-control',
                                                               'placeholder': 'Дата смерти (ГГГГ-ММ-ДД)'})}


class MoviesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['actor'].empty_label = 'Актер не выбран'

    class Meta:
        model = Movie
        actor = forms.ModelChoiceField(queryset=Person.objects.all_with_prefetch_films(), to_field_name='actor')
        fields = ['title', 'genre', 'year', 'preview', 'actor']
        widgets = {'title': TextInput(attrs={'class': 'form-input', 'placeholder': 'Название фильма'}),
                   'genre': TextInput(attrs={'class': 'form-input', 'placeholder': 'Жанр'}),
                   'preview': forms.Textarea(attrs={'cols': 50, 'rows': 10, 'placeholder': 'Описание фильма'}),
                   'year': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Год выпуска'})}
