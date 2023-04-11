from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')


class TitleAdmin(admin.ModelAdmin):
    def list_genres(self, title):
        return title.genres.values_list('name', flat=True)
    list_genres.short_description = 'Список жанров'
    list_display = (
        'pk', 'name', 'year', 'description', 'list_genres', 'category'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
