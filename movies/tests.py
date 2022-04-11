from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from movies.models import Movie


# Create your tests here.
class MoviesTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test@gmail.com")
        self.user.set_password("azerty01")
        self.user.save()
        self.movie = Movie.objects.create(title_vf="Dune")

    def test_movie_list_view_anonymous_user(self):
        url = reverse("movies:movies_list")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/movies_list.html")
        self.assertNotIn("PROFIL", response.content.decode())

    def test_movie_list_view_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("movies:movies_list")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/movies_list.html")
        self.assertIn("PROFIL", response.content.decode())

    def test_movie_detail_view_anonymous_user(self):
        url = reverse("movies:movies_detail", kwargs={"pk": self.movie.pk,
                                                      "slug": self.movie.slug})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/movies_detail.html")
        self.assertNotIn("PROFIL", response.content.decode())
        self.assertIn(self.movie.title_vf, response.content.decode())

    def test_movie_detail_view_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("movies:movies_detail", kwargs={"pk": self.movie.pk,
                                                      "slug": self.movie.slug})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/movies_detail.html")
        self.assertIn("PROFIL", response.content.decode())
        self.assertIn(self.movie.title_vf, response.content.decode())
