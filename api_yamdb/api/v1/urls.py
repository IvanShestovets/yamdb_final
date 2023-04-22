from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    sign_up,
    get_token,
    UsersViewSet,
    CategoriesViewSet,
    ReviewViewSet,
    TitlesViewSet,
    CommentViewSet,
    GenreViewSet
)


v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_urlpatterns)),
]
