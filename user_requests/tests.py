from django.test import TestCase


# Create your tests here.
from django.urls import reverse

from accounts.models import CustomUser
from movies.models import Movie
from user_requests.models import BluRayRequest


class UserRequestsTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test@gmail.com")
        self.user.set_password("azerty01")
        self.user.save()
        self.movie = Movie.objects.create(title_vf="Dune",
                                          movie_image="fake.jpg")
        self.bluray_request = BluRayRequest.objects.create(user=self.user,
                                                           amazon_link="https://www.amazon.fr/Dune-UHD-4K/dp/B09GKPXY36/")

    def test_user_requests_view_anonymous_user(self):
        url = reverse("user_requests:user_requests", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 302)
        self.assertNotIn('<div class="favorite-wrapper">',
                         response.content.decode())

    def test_user_requests_view_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("user_requests:user_requests", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_requests/user-requests.html")
        self.assertIn("PROFIL", response.content.decode())
        self.assertIn("Toutes vos demandes", response.content.decode())
        self.assertIn("B09GKPXY36", response.content.decode())
        self.assertIn('<div class="favorite-wrapper">',
                      response.content.decode())
