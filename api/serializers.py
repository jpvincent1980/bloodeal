from rest_framework.serializers import ModelSerializer

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


class CustomUserSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email", "pseudo",
                  "join_date"]


class BluRaySerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = BluRay
        fields = ["id", "movie", "slug", "title", "uhd", "vf", "forced_sub",
                  "ean", "amazon_asin", "amazon_aff_link", "release_date",
                  "bluray_image", "requested_by", "date_created",
                  "date_updated"]


class DealSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = Deal
        fields = ["id", "bluray", "amazon_aff_link", "created_by", "status",
                  "price", "start_date", "end_date", "date_created",
                  "date_updated"]


class MovieSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = Movie
        fields = ["id", "title_vf", "title_vo", "slug", "release_year",
                  "imdb_id", "movie_image", "requested_by", "date_created",
                  "date_updated"]


class MovieActorSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = MovieActor
        fields = ["id", "movie", "actor", "date_created", "date_updated"]


class MovieDirectorSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = MovieDirector
        fields = ["id", "movie", "director", "date_created", "date_updated"]


class PeopleSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = People
        fields = ["id", "first_name", "last_name", "slug", "birth_date",
                  "death_date", "imdb_id", "people_image", "requested_by",
                  "date_created", "date_updated"]


class FavoriteBluRaySerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = FavoriteBluRay
        fields = ["id", "user", "bluray", "date_created", "date_updated"]


class FavoriteMovieSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = FavoriteMovie
        fields = ["id", "user", "movie", "date_created", "date_updated"]


class FavoritePeopleSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = FavoritePeople
        fields = ["id", "user", "people", "date_created", "date_updated"]


class BluRayRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = BluRayRequest
        fields = ["id", "user", "amazon_link", "asin", "bluray", "status",
                  "date_created", "date_updated"]


class MovieRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = MovieRequest
        fields = ["id", "user", "imdb_link", "imdb_id", "title_vf", "title_vo",
                  "release_year", "movie", "status",
                  "date_created", "date_updated"]


class PeopleRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = PeopleRequest
        fields = ["id", "user", "imdb_link", "imdb_id",
                  "first_name", "last_name", "birth_date", "death_date",
                  "people", "status", "date_created", "date_updated"]


class DealRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes CustomUser instances.
    """
    class Meta:
        model = DealRequest
        fields = ["id", "user", "bluray", "amazon_link", "asin", "price",
                  "deal", "status", "date_created", "date_updated"]
