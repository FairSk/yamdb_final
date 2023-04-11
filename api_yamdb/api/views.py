from api.filters import TitleFilter
from api.mixins import CreateDestroyListMixin
from api.permissions import (IsAdmin, IsAdminOrModeratorOrAuthor,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ProfileSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleSerializer, TitleSerializerReadOnly,
                             TokenSerializer, UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    """New User Registration
    Receiving a confirmation code to the sent_mail.
    Permissions: Available without a token.
    The email and username fields must be unique."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, created = User.objects.get_or_create(**serializer.validated_data)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDb registration',
        message=f'Your confirmation code: {confirmation_code}',
        from_email=None,
        recipient_list=(user.email,),
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Receiving JWT-TOKEN
    Getting a JWT token in exchange for username and confirmation code.
    Permissions: Available without a token."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Getting a list of all users
    Access rights(permissions): Administrator
    Searching by username (username)
    Show profile use get and patch
    Access rights:IsAuthenticated """
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=ProfileSerializer
    )
    def set_profile(self, request, pk=None):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateDestroyListMixin, GenericViewSet):
    """Getting a list of all categories
    Permissions: Available without a token
    Searching by name"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListMixin, GenericViewSet):
    """Getting a list of all genres
    Permissions: Available without a token
    Searching by name"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Getting a list of all titles with rating
    Permissions: Available without a token"""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleSerializerReadOnly
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Getting a list of all titles with rating
    Permissions: Available without a token
    the function provides with access rights to add a new review,
    receive or delete a review by title_id """
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            return (IsAdminOrModeratorOrAuthor(),)
        return (IsAuthenticatedOrReadOnly(),)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Getting a list of all Comments
    Permissions: Available without a token
    the function provides with access rights to add a new comment,
    receive or delete a comment by review_id"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            return (IsAdminOrModeratorOrAuthor(),)
        return (IsAuthenticatedOrReadOnly(),)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )
