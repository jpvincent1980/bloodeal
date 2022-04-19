from rest_framework.viewsets import ModelViewSet

from .serializers import (
    CustomUserSerializer,
    BluRaySerializer,
    MovieSerializer,
    MovieDirectorSerializer,
    MovieActorSerializer,
    PeopleSerializer,
    DealSerializer,
    FavoriteMovieSerializer,
    FavoritePeopleSerializer,
    FavoriteBluRaySerializer,
    PeopleRequestSerializer,
    MovieRequestSerializer,
    BluRayRequestSerializer,
    DealRequestSerializer)

from .permissions import IsAnonymous, IsRequester, IsUser, IsAdmin

from accounts.models import CustomUser
from blurays.models import BluRay
from deals.models import Deal
from movies.models import Movie, MovieActor, MovieDirector
from people.models import People
from profiles.models import FavoriteBluRay, FavoriteMovie, FavoritePeople
from user_requests.models import (
    BluRayRequest,
    MovieRequest,
    PeopleRequest,
    DealRequest)


# Create your views here.
class CustomUserViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete CustomUser
    instances.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdmin]


class BluRayViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete BluRay
    instances.
    """
    queryset = BluRay.objects.all()
    serializer_class = BluRaySerializer
    permission_classes = [IsAnonymous | IsRequester | IsAdmin]


class MovieViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete Movie
    instances.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAnonymous | IsRequester | IsAdmin]


class MovieDirectorViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete MovieDirector
    instances.
    """
    queryset = MovieDirector.objects.all()
    serializer_class = MovieDirectorSerializer
    permission_classes = [IsAnonymous]


class MovieActorViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete MovieActor
    instances.
    """
    queryset = MovieActor.objects.all()
    serializer_class = MovieActorSerializer
    permission_classes = [IsAnonymous]


class PeopleViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete People
    instances.
    """
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    permission_classes = [IsAnonymous | IsRequester | IsAdmin]


class DealViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete Deal
    instances.
    """
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAnonymous | IsRequester | IsAdmin]


class FavoriteMovieViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete FavoriteMovie
    instances.
    """
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializer
    permission_classes = [IsUser | IsAdmin]


class FavoritePeopleViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete FavoritePeople
    instances.
    """
    queryset = FavoritePeople.objects.all()
    serializer_class = FavoritePeopleSerializer
    permission_classes = [IsUser | IsAdmin]


class FavoriteBluRayViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete FavoriteBluRay
    instances.
    """
    queryset = FavoriteBluRay.objects.all()
    serializer_class = FavoriteBluRaySerializer
    permission_classes = [IsUser | IsAdmin]


class PeopleRequestViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete PeopleRequest
    instances.
    """
    queryset = PeopleRequest.objects.all()
    serializer_class = PeopleRequestSerializer
    permission_classes = [IsUser | IsAdmin]


class MovieRequestViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete MovieRequest
    instances.
    """
    queryset = MovieRequest.objects.all()
    serializer_class = MovieRequestSerializer
    permission_classes = [IsUser | IsAdmin]


class BluRayRequestViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete BluRayRequest
    instances.
    """
    queryset = BluRayRequest.objects.all()
    serializer_class = BluRayRequestSerializer
    permission_classes = [IsUser | IsAdmin]


class DealRequestViewSet(ModelViewSet):
    """
    A custom ViewSet to list, retrieve, create, update and delete DealRequest
    instances.
    """
    queryset = DealRequest.objects.all()
    serializer_class = DealRequestSerializer
    permission_classes = [IsUser | IsAdmin]
