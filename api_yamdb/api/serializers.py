from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignUpSerializer(serializers.Serializer):
    """Serializer created for Sigh Up POST
    endpoint for checking: /api/v1/auth/signup/
    two main arguments: email and username
    exception:you cant create username with "me"
    validation optimizes Sigh Up
    """
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (User.objects.filter(username=username)
                .exclude(email=email).exists()):
            raise serializers.ValidationError('This username is already taken')
        if (User.objects.filter(email=email)
                .exclude(username=username).exists()):
            raise serializers.ValidationError('This email is already taken')
        return data


class TokenSerializer(serializers.Serializer):
    """Serializer created for TOKEN
    endpoint for checking: /api/v1/auth/token/
    two main arguments: username and confirmation code
    The user sends a POST request with the username and confirmation_code
    parameters to the endpoint /api/v1/auth/token/ ,
    in response to the request he receives a token (JWT token)"""
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    confirmation_code = serializers.CharField(max_length=64)


class UserSerializer(serializers.ModelSerializer):
    """Serializer created for User
    Used class User for model"""
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class ProfileSerializer(UserSerializer):
    """Serializer created for Profile
    Displaying the selected role"""
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer created for Category
    Used class Category for model, excluded field id """
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer created for Genre
    Used class Genre for model, excluded field id """
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Serializer created for Title
    Used class Title for model
    two main arguments: genre and category"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class TitleSerializerReadOnly(serializers.ModelSerializer):
    """Serializer created for Title
    Used class Title for model
    three main arguments: rating, genre and category
    works based on permissions"""
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer created for Review
    Used class Review for model
    the main argument: author
    validation optimizes that only one review per title is allowed"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            if author.reviews.filter(title=title).exists():
                raise serializers.ValidationError(
                    'Only one review per title is allowed')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer created for Comment
    Used class Comment for model"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
