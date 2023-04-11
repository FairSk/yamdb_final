from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

error_message = 'Error'
success_message = 'Success'
start_message = 'Importing data'


class Command(BaseCommand):
    """Imports data from csv files into SQLite3 DataBase."""

    help = 'Команда для создания БД на основе имеющихся csv файлов'

    def genre_create(row):
        Genre.objects.create(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )

    def category_create(row):
        Category.objects.create(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )

    def title_create(row):
        Title.objects.create(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category'])
        )

    def genre_title_create(row):
        Title.genres.through.objects.create(
            id=row['id'],
            title_id=row['title_id'],
            genre_id=row['genre_id']
        )

    def user_create(row):
        User.objects.create(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name']
        )

    def comment_create(row):
        Comment.objects.create(
            id=row['id'],
            review_id=row['review_id'],
            text=row['text'],
            author=User.objects.get(id=row['author']),
            pub_date=['pub_date']
        )

    def review_create(row):
        title, _ = Title.objects.get_or_create(id=row['title_id'])
        Review.objects.create(
            id=row['id'],
            title_id=title.pk,
            text=row['text'],
            author=User.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date']
        )

    ACTIONS = [
        (genre_create, Genre, 'genre.csv'),
        (category_create, Category, 'category.csv'),
        (title_create, Title, 'titles.csv'),
        (genre_title_create, Title.genres.through, 'genre_title.csv'),
        (user_create, User, 'users.csv'),
        (review_create, Review, 'review.csv'),
        (comment_create, Comment, 'comments.csv'),
    ]

    def handle(self, *args, **options):
        print(start_message)
        for func, model, file in self.ACTIONS:
            if model.objects.exists():
                print(error_message)
            else:
                for row in DictReader(
                    open('static/data/' + file, encoding='utf8')
                ):
                    func(row)

        print(success_message)
