'''Команда для заполнения данных в БД из CSV файлов.'''

from csv import DictReader

from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

ENCODING = 'utf-8'


class Command(BaseCommand):

    help = "Импорт данных из genre.csv"

    def handle(self, *args, **options):

        try:
            print("Загрузка данных пользователей...")

            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\users.csv',
                    encoding=ENCODING
                )
            ):
                user = User(
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                user.save()

            print("Загрузка данных пользователей завершена!")

            print("Загрузка данных жанров...")
            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\genre.csv',
                    encoding=ENCODING
                )
            ):
                genre = Genre(name=row['name'], slug=row['slug'])
                genre.save()
            print("Загрузка данных жанров завершена!")

            print("Загрузка данных категорий...")
            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\category.csv',
                    encoding=ENCODING
                )
            ):
                category = Category(name=row['name'], slug=row['slug'])
                category.save()
            print("Загрузка данных категорий завершена!")

            print("Загрузка данных произведений...")
            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\titles.csv',
                    encoding=ENCODING
                )
            ):
                title = Title(
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
                title.save()
            print("Загрузка данных произведений завершена!")

            print("Загрузка данных жанров произведений...")
            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\genre_title.csv',
                    encoding=ENCODING
                )
            ):
                genre_title = GenreTitle(
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )
                genre_title.save()
            print("Загрузка данных жанров произведений завершена!")

            print("Загрузка данных отзывов произведений...")
            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\review.csv',
                    encoding=ENCODING
                )
            ):
                author_id = str(int(row['author'][-1]) + 1)
                review = Review(
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=author_id,
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                review.save()
            print("Загрузка данных отзывов завершена!")

            print("Загрузка данных комментариев произведений...")
            for row in DictReader(
                open(
                    r'..\api_yamdb\static\data\comments.csv',
                    encoding=ENCODING
                )
            ):
                author_id = str(int(row['author'][-1]) + 1)
                comment = Comment(
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=author_id,
                    pub_date=row['pub_date']
                )
                comment.save()
            print("Загрузка данных комментариев завершена!")

        except IntegrityError:
            return (
                "Данные уже загружены!"
            )
