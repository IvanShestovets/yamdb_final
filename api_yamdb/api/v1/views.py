from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from users.models import User
from reviews.models import Title, Category, Genre, Review
from api.v1.mixins import CreateListDestroyViewSet
from api.v1.serializers import (
    UserRegisterSerializer,
    UserGetTokenSerializer,
    UserProfileSerializer,
    UsersSerializer,
    TitlesCreateSerializer,
    TitlesViewSerializer,
    ReviewSerializer,
    CategoriesSerializer,
    CommentSerializer,
    GenreSerializer
)
from api.v1.permissions import (
    IsAdminOrSuperUser,
    IsAuthorAdminModeratorOrReadOnly,
    IsAdminOrReadOnly
)
from api.v1.filters import TitleFilter


@api_view(['POST'])
def sign_up(request):
    '''Регистрация пользователя и
    получение кода подтверждения в почту
    '''

    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = User.objects.filter(**serializer.data).last()
    if user:
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Ваш код подтверждения',
            f'Код {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    '''Получение токена'''

    serializer = UserGetTokenSerializer(data=request.data)
    if serializer.is_valid():
        if 'error' in serializer.validated_data:
            return Response(
                serializer.validated_data,
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    '''Получение, создание, изменение, удаление
    пользователей администратором или суперюзером
    '''

    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOrSuperUser, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        '''Создание пользователя.'''
        serializer.save()

    def perform_update(self, serializer):
        '''Изменение профайла пользователя.'''
        if self.request.user.role != User.UserRole.ADMIN:
            raise PermissionDenied('Изменение чужого профиля запрещено!')
        serializer.save()

    def perform_destroy(self, serializer):
        '''Удаление пользователя.'''
        serializer.delete()

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated, )
    )
    def get_user_profile(self, request):
        '''Личный профайл пользователя. Возможен просмотр и изменение.'''
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserProfileSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CategoriesViewSet(CreateListDestroyViewSet):
    '''Создание, получение, удаление категории.
    Просмотр доступен всем. Создание и удаление
    только администратору.'''

    queryset = Category.objects.all().order_by('-id')
    lookup_field = 'slug'
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name',)


class GenreViewSet(CreateListDestroyViewSet):
    '''Создание, получение, удаление жанра.
    Просмотр доступен всем. Создание и удаление
    только администратору.'''

    queryset = Genre.objects.all().order_by('-id')
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name',)


class TitlesViewSet(viewsets.ModelViewSet):
    '''Создание, получение, изменение и удаление произведения.
    Просмотр доступен всем. Создание, изменение и удаление
    только администратору.'''

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesViewSerializer
        return TitlesCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''Создание, получение, изменение и удаление отзыва к произведению.
    Просмотр доступен всем. Создание - аутентифицированным пользователям,
    изменение и удаление только авторам, админам и модераторам.'''

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    '''Создание, получение, изменение и удаление комментария к отзыву.
    Просмотр доступен всем. Создание - аутентифицированным пользователям,
    изменение и удаление только авторам, админам и модераторам.'''

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
