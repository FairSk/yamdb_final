from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year


class User(AbstractUser):
    """
    Custom user model. Supports all CRUD functions.
    Model fields:
        email: user's email, required field,
        bio: user's description, type - string, optional field,
        role: user's role, type - string, required field.
    """
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        max_length=254,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_is_not_me'
            )
        ]


class Category(models.Model):
    """
    Category model. Supports all CRUD functions.
    Model fields:
        name: category's name, type - string, required field,
        slug: category's slug, type - string, required field.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Genre model. Supports all CRUD functions.
    Model fields:
        name: genre's name, type - string, required field,
        slug: genre's slug, type - string, required field.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Title model. Supports all CRUD functions.
    Model fields:
        name: title's name, type - string, required field,
        year: title's release date, type - int, required field,
        description: title's description, type - string, optional field,
        genre: title's genre, type - Genre class instance, required field,
        category: title's category, type - Category class instance, optional
        field.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Review model. Supports all CRUD functions.
    Model fields:
        title: review's title, type - Title class instance
        required field,
        text:  review's text, type - string, required field,
        author: review's author, type - User class instnce, required field,
        score: review's score, type - int, required field,
        pub_date: review's publication date, type - datetime field,
        automatically fullfield.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название'
    )
    text = models.TextField(max_length=10000, verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Score must be between 1 and 10.'),
            MaxValueValidator(10, message='Score must be between 1 and 10.')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comment model. Supports all CRUD functions.
    Model fields:
        review: comment's review, type - Review class instance
        required field,
        text:  comment's text, type - string, required field,
        author: comment's author, type - User class instnce, required field,
        pub_date: comment's publication date, type - datetime field,
        automatically fullfield.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(max_length=1000, verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
