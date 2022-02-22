from django.core.management.base import BaseCommand
from faker import Faker
from main.models import Movie, Person


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--len', type=int, default=4)
        parser.add_argument('--year', type=int, default=2000)

    def handle(self, *args, **options):
        faker = Faker()
        self.stdout.write('Start adding films')
        for m in range(options['len']):
            self.stdout.write('... add movie ...')
            movie = Movie()
            person = Person()
            faker_title_for_movie = ' '.join(faker.text().split()[:3])
            faker_title_for_person = ' '.join(faker.text().split()[:2])
            movie.title = faker_title_for_movie
            movie.year = options['year']
            movie.actor = faker.name()
            movie.preview = faker.text()
            person.name = faker_title_for_person
            movie.save()
            person.save()
            self.stdout.write(f'New_Movie: "{movie.title}" director: {person.name} ({movie.year})')
        self.stdout.write('End :=)')
