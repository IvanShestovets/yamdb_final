import datetime as dt

from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        allow_blank=False,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, attrs):
        username = attrs['username']
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть me.'
            )
        if attrs['username'] == attrs['email']:
            raise serializers.ValidationError(
                'Ник не может совпадать с почтой!')

        user_check = User.objects.filter(**attrs).exists()
        if not user_check:
            user = User.objects.create(**attrs)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Ваш код подтверждения',
                f'Код {confirmation_code}',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )
        return attrs


class UserGetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']

        try:
            self.user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            return ({
                'error': 'Пользователь не найден!',
            })

        if not self.user.is_active:
            raise serializers.ValidationError(
                'Аккаунт заблокированный.'
            )

        if default_token_generator.check_token(self.user, confirmation_code):
            token = AccessToken.for_user(self.user)
            update_last_login(None, self.user)
            return ({
                'token': str(token),
            })
        raise serializers.ValidationError(
            'Недействительный код подтверждения!'
        )


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.UserRole.choices,
        read_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        allow_blank=False,
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(
        choices=User.UserRole.choices,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategoriesSerializer(serializers.ModelSerializer):
    '''Категории, описание.'''

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    '''Жанры, описание.'''

    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitlesCreateSerializer(serializers.ModelSerializer):
    '''Запись информации о произведении.'''

    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all(),
        allow_null=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год')
        return value


class TitlesViewSerializer(serializers.ModelSerializer):
    '''Получения информации о произведении.'''

    category = CategoriesSerializer(
        many=False,
        required=False,
        read_only=True
    )
    rating = serializers.SerializerMethodField(
        required=False,
        allow_null=True,
        read_only=True
    )
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        if len(obj.reviews.all()) != 0:
            return int(obj.reviews.aggregate(Avg('score'))['score__avg'])
        return None


class ReviewSerializer(serializers.ModelSerializer):
    '''Отзывы.'''

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ['title', ]

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Пожалуйста, оцените произведение по шкале от 1 до 10'
            )
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            context_request = self.context['request']
            title_id = context_request.parser_context['kwargs']['title_id']
            author = self.context['request'].user
            if author.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили свой отзыв.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Комментарии к отзывам.'''

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'title',)

    def validate_text(self, value):
        if type(value) != str:
            raise serializers.ValidationError(
                'Некорректные данные!'
            )
        return value
