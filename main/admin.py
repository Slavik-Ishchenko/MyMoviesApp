from django.contrib import admin

from .models import Movie, Roles, Person


class RoleInLine(admin.StackedInline):
    model = Roles
    extra = 1
    autocomplete_fields = ('person', 'movie')


class DirectorInLine(admin.StackedInline):
    model = Movie
    fk_name = 'actor'
    verbose_name = 'Актер'
    verbose_name_plural = 'Актеры'
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = [RoleInLine]
    list_display = ('title', 'genre', 'year', 'rating')
    list_filter = ('rating',)
    fields = (('title', 'genre', 'year',), ('runtime', 'rating'), 'preview', 'actor',)
    autocomplete_fields = ('actor',)
    search_fields = ('title',)


class ActorInLine(admin.StackedInline):
    model = Movie
    verbose_name = 'Актер'
    verbose_name_plural = 'Актеры'
    extra = 1
    autocomplete_fields = ('movie',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'died',)
    inlines = [RoleInLine, DirectorInLine]
    search_fields = ('name',)

    def show_name(self, obj):
        return "{}".format(obj.name)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Person, PersonAdmin)
