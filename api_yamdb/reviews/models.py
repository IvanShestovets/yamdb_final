from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from reviews.validators import validate_year


class Genre(models.Model):
    '''Модель жанров.'''

    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    '''Модель категорий.'''

    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    '''Модель Произведение'''

    name = models.TextField(max_length=256)
    year = models.IntegerField(
        'Год издания',
        validators=[validate_year],
        help_text='Введите год издания'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Тип произведения',
        help_text='Введите тип произведения',
        null=True,
        blank=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание пороизведения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    '''Промежуточная модель для отношений жанров к произведениям.'''

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    '''Модель отзывов.'''

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    '''Модель комментариев к отзывам.'''

    text = models.TextField(
        'Текст комментария', max_length=100
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'

    def __str__(self) -> str:
        return self.text[:15]
