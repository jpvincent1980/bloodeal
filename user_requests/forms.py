from django.forms import ModelForm

from user_requests.models import BluRayRequest, MovieRequest, PeopleRequest


class BluRayCreationForm(ModelForm):
    class Meta:
        model = BluRayRequest
        fields = ["amazon_link", "user", "status"]


class MovieCreationForm(ModelForm):
    class Meta:
        model = MovieRequest
        fields = ["imdb_link", "user", "status"]


class PeopleCreationForm(ModelForm):
    class Meta:
        model = PeopleRequest
        fields = ["imdb_link", "user", "status"]
