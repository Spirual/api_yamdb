import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.base import ModelBase

from reviews.models import (
    Category,
    Title,
    Comment,
    Genre,
    Review,
)

User = get_user_model()


def create_obj_wo_fk(model_name: ModelBase, row: dict):
    model_name.objects.get_or_create(**row)


def import_title(_, row: dict):
    category = Category.objects.get(id=row['category'])
    row.update(category=category)
    Title.objects.create(**row)


def import_title_genre(_, row: dict):
    title = Title.objects.get(id=row['title_id'])
    genre = Genre.objects.get(id=row['genre_id'])
    title.genre.add(genre)


def import_review(_, row: dict):
    title = Title.objects.get(id=row['title_id'])
    author = User.objects.get(id=row['author'])
    row.update(title=title, author=author)
    Review.objects.create(**row)


def import_comment(_, row: dict):
    review = Review.objects.get(id=row['review_id'])
    author = User.objects.get(id=row['author'])
    row.update(review=review, author=author)
    Comment.objects.create(**row)


mapping = {
    'category.csv': (Category, create_obj_wo_fk),
    'genre.csv': (Genre, create_obj_wo_fk),
    'users.csv': (User, create_obj_wo_fk),
    'titles.csv': (None, import_title),
    'review.csv': (None, import_review),
    'comments.csv': (None, import_comment),
    'genre_title.csv': (None, import_title_genre),
}


class Command(BaseCommand):
    help = 'Поместите файлы в директорию static/data/'
    directory_path = r'static/data/'

    def get_list_of_dicts(self, file_name: str) -> list[dict]:
        """Возвращает список словарей, по словарю на строку файла."""
        file = str(self.directory_path + file_name)
        with open(file=file, encoding='utf-8') as r_file:
            reader = csv.DictReader(r_file,)
            list_of_dicts = []
            for row in reader:
                list_of_dicts.append(row)
            return list_of_dicts

    def distributor(self, file_name: str, list_of_dicts: list[dict]) -> None:
        """Вызывает нажную функцию для создания экземпляра класса."""
        model_name = mapping[file_name][0]
        import_counter = 0
        for dict in list_of_dicts:
            mapping[file_name][1](model_name, dict)
            import_counter += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Из {file_name} импортировано {import_counter} объектов.'
            )
        )

    @transaction.atomic
    def handle(self, *args, **options):
        for file_name, _ in mapping.items():
            list_of_dicts = self.get_list_of_dicts(file_name)
            self.distributor(file_name, list_of_dicts)
        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))
