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


def generate_initialized_request_forms(user, status="1"):
    bluray_request_form = BluRayCreationForm(initial={"user": user,
                                                      "status": status},
                                             auto_id="bluray_request_%s")
    movie_request_form = MovieCreationForm(initial={"user": user,
                                                    "status": status},
                                           auto_id="movie_request_%s")
    people_creation_form = PeopleCreationForm(initial={"user": user,
                                                       "status": status},
                                              auto_id="people_request_%s")
    requests_forms = {"bluray_request_form": bluray_request_form,
                      "movie_request_form": movie_request_form,
                      "people_request_form": people_creation_form}
    return requests_forms
