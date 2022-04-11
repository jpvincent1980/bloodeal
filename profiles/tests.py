from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from blurays.models import BluRay
from movies.models import Movie
from people.models import People


# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test@gmail.com")
        self.user.set_password("azerty01")
        self.user.save()
        self.bluray = BluRay.objects.create(title="Dune 4K")
        self.movie = Movie.objects.create(title_vf="Dune",
                                          movie_image="fake.jpg")
        self.people = People.objects.create(first_name="Denis",
                                            last_name="Villeneuve")

    def test_favorites_list_view_anonymous_user(self):
        url = reverse("profiles:favorites_list")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 302)
        self.assertNotIn('<div class="favorite-wrapper">',
                         response.content.decode())

    def test_favorites_list_view_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("profiles:favorites_list")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/favorites_list.html")
        self.assertIn("PROFIL", response.content.decode())
        self.assertIn('<div class="favorite-wrapper">',
                      response.content.decode())

    def test_profile_update_anonymous_user(self):
        url = reverse("profiles:profile_update")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 302)
        self.assertNotIn('<div class="favorite-wrapper">',
                         response.content.decode())

    def test_profile_update_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("profiles:profile_update")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/user_update.html")
        self.assertIn("VOTRE PROFIL", response.content.decode())
        self.assertIn('<div class="favorite-wrapper">',
                      response.content.decode())
