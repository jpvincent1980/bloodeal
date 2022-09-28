from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

from .views import (
    CustomUserViewSet,
    BluRayViewSet,
    MovieViewSet,
    MovieDirectorViewSet,
    MovieActorViewSet,
    PeopleViewSet,
    DealViewSet,
    FavoriteBluRayViewSet,
    FavoriteMovieViewSet,
    FavoritePeopleViewSet,
    BluRayRequestViewSet,
    MovieRequestViewSet,
    PeopleRequestViewSet,
    DealRequestViewSet)

app_name = "api"

router = DefaultRouter()
router.APIRootView.__name__ = "Bloodeal"
router.APIRootView.__doc__ = "API de l'application Bloodeal"
router.register(r'users', CustomUserViewSet)
router.register(r'blurays', BluRayViewSet)
router.register(r'movies', MovieViewSet, basename="movies")
router.register(r'movies_directors', MovieDirectorViewSet)
router.register(r'movies_actors', MovieActorViewSet)
router.register(r'people', PeopleViewSet)
router.register(r'deals', DealViewSet)
router.register(r'favorite_blurays', FavoriteBluRayViewSet)
router.register(r'favorite_movies', FavoriteMovieViewSet)
router.register(r'favorite_people', FavoritePeopleViewSet)
router.register(r'bluray_requests', BluRayRequestViewSet)
router.register(r'movie_requests', MovieRequestViewSet)
router.register(r'people_requests', PeopleRequestViewSet)
router.register(r'deal_requests', DealRequestViewSet)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('login/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('v1/', include(router.urls)),
    path('v1/', router.APIRootView.as_view(), name="v1"),
]
