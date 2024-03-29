from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField
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
    A custom ModelSerializer that serializes BluRay instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["requested_by"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["requested_by"].queryset = CustomUser.objects.all()

    requested_by = SlugRelatedField(queryset=CustomUser.objects.all(),
                                    slug_field="pseudo")
    movie = SlugRelatedField(read_only=True,
                             slug_field="title_vf")

    class Meta:
        model = BluRay
        fields = ["id", "movie", "slug", "title", "uhd", "vf", "forced_sub",
                  "ean", "amazon_asin", "amazon_aff_link", "release_date",
                  "bluray_image", "requested_by", "date_created",
                  "date_updated"]


class DealSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes Deal instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["requested_by"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["requested_by"].queryset = CustomUser.objects.all()

    requested_by = SlugRelatedField(queryset=CustomUser.objects.all(),
                                    slug_field="pseudo")
    bluray = SlugRelatedField(read_only=True,
                              slug_field="title")

    class Meta:
        model = Deal
        fields = ["id", "bluray", "amazon_aff_link", "requested_by", "status",
                  "price", "start_date", "end_date", "date_created",
                  "date_updated"]


class MovieSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes Movie instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["requested_by"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["requested_by"].queryset = CustomUser.objects.all()

    requested_by = SlugRelatedField(queryset=CustomUser.objects.all(),
                                    slug_field="pseudo")

    class Meta:
        model = Movie
        fields = ["id", "title_vf", "title_vo", "slug", "release_year",
                  "imdb_id", "movie_image", "requested_by", "date_created",
                  "date_updated"]


class MovieActorSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes MovieActor instances.
    """
    movie = SlugRelatedField(read_only=True,
                             slug_field="title_vf")
    actor = SlugRelatedField(read_only=True,
                             slug_field="people_full_name")

    class Meta:
        model = MovieActor
        fields = ["id", "movie", "actor", "date_created", "date_updated"]


class MovieDirectorSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes MovieDirector instances.
    """
    movie = SlugRelatedField(read_only=True,
                             slug_field="title_vf")
    director = SlugRelatedField(read_only=True,
                                slug_field="people_full_name")

    class Meta:
        model = MovieDirector
        fields = ["id", "movie", "director", "date_created", "date_updated"]


class PeopleSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes People instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["requested_by"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["requested_by"].queryset = CustomUser.objects.all()

    requested_by = SlugRelatedField(queryset=CustomUser.objects.all(),
                                    slug_field="pseudo")

    class Meta:
        model = People
        fields = ["id", "first_name", "last_name", "slug", "birth_date",
                  "death_date", "imdb_id", "people_image", "requested_by",
                  "date_created", "date_updated"]


class FavoriteBluRaySerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes FavoriteBluRay instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")
    bluray = SlugRelatedField(read_only=True,
                              slug_field="title")

    class Meta:
        model = FavoriteBluRay
        fields = ["id", "user", "bluray", "date_created", "date_updated"]


class FavoriteMovieSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes FavoriteMovie instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super(FavoriteMovieSerializer, self).__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")
    movie = SlugRelatedField(queryset=Movie.objects.all(),
                             slug_field="title_vf")

    class Meta:
        model = FavoriteMovie
        fields = ["id", "user", "movie", "date_created", "date_updated"]


class FavoritePeopleSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes FavoritePeople instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")
    people = SlugRelatedField(queryset=People.objects.all(),
                              slug_field="people_full_name")

    class Meta:
        model = FavoritePeople
        fields = ["id", "user", "people", "date_created", "date_updated"]


class BluRayRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes BluRayRequest instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")

    class Meta:
        model = BluRayRequest
        fields = ["id", "user", "amazon_link", "asin", "bluray", "status",
                  "date_created", "date_updated"]


class MovieRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes MovieRequest instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")

    class Meta:
        model = MovieRequest
        fields = ["id", "user", "imdb_link", "imdb_id", "title_vf", "title_vo",
                  "release_year", "movie", "status",
                  "date_created", "date_updated"]


class PeopleRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes PeopleRequest instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")

    class Meta:
        model = PeopleRequest
        fields = ["id", "user", "imdb_link", "imdb_id",
                  "first_name", "last_name", "birth_date", "death_date",
                  "people", "status", "date_created", "date_updated"]


class DealRequestSerializer(ModelSerializer):
    """
    A custom ModelSerializer that serializes DealRequest instances.
    """
    def __init__(self, *args, **kwargs):
        current_user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if not current_user.is_staff:
            self.fields["user"].queryset = CustomUser.objects.filter(pk=current_user.pk)
        else:
            self.fields["user"].queryset = CustomUser.objects.all()

    user = SlugRelatedField(queryset=CustomUser.objects.all(),
                            slug_field="pseudo")
    bluray = SlugRelatedField(read_only=True,
                              slug_field="title")

    class Meta:
        model = DealRequest
        fields = ["id", "user", "bluray", "amazon_link", "asin", "price",
                  "deal", "status", "date_created", "date_updated"]
