import csv

from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import (
    Category,
    Title,
    Comment,
    Genre,
    Review,
)

User = get_user_model()


def import_title(row):
    category = Category.objects.get(id=row['category'])
    row.update(category=category)
    Title.objects.create(**row)


def import_title_genre(row):
    title = Title.objects.get(id=row['title_id'])
    genre = Genre.objects.get(id=row['genre_id'])
    title.genre.add(genre)


def import_review(row):
    title = Title.objects.get(id=row['title_id'])
    author = User.objects.get(id=row['author'])
    row.update(title=title, author=author)
    Review.objects.create(**row)


def import_comment(row):
    review = Review.objects.get(id=row['review_id'])
    author = User.objects.get(id=row['author'])
    row.update(review=review, author=author)
    Comment.objects.create(**row)


file_names_and_model = {
    'category.csv': (Category,),
    'genre.csv': (Genre,),
    'users.csv': (User,),
    'titles.csv': (Title, import_title),
    'review.csv': (Review, import_review),
    'comments.csv': (Comment, import_comment),
    'genre_title.csv': (Title, import_title_genre),
}


class Command(BaseCommand):
    help = 'Поместите файлы в директорию static/data/'
    directory_path = r'static/data/'

    def importer(self, file_name):
        file = str(self.directory_path + file_name)
        with open(file=file, encoding='utf-8') as r_file:
            reader = csv.DictReader(r_file,)
            import_counter = 0
            for row in reader:
                try:
                    file_names_and_model[file_name][0].objects.get_or_create(
                        **row
                    )
                except ValueError:
                    file_names_and_model[file_name][1](row)
                except FieldError:
                    import_title_genre(row)
                import_counter += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Из {file_name} импортировано {import_counter} объектов.'
            )
        )

    @transaction.atomic
    def handle(self, *args, **options):
        for file_name, _ in file_names_and_model.items():
            self.importer(file_name)
        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))
