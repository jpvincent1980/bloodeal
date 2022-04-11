from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from blurays.models import BluRay


class BluRaysTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test@gmail.com")
        self.user.set_password("azerty01")
        self.user.save()
        self.bluray = BluRay.objects.create(title="Dune 4K")

    def test_bluray_list_view_anonymous_user(self):
        url = reverse("blurays:blurays_list")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blurays/blurays_list.html")
        self.assertNotIn("PROFIL", response.content.decode())

    def test_bluray_list_view_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("blurays:blurays_list")
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blurays/blurays_list.html")
        self.assertIn("PROFIL", response.content.decode())

    def test_bluray_detail_view_anonymous_user(self):
        url = reverse("blurays:blurays_detail", kwargs={"pk": self.bluray.pk,
                                                        "slug": self.bluray.slug})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blurays/blurays_detail.html")
        self.assertNotIn("PROFIL", response.content.decode())
        self.assertIn(self.bluray.title, response.content.decode())

    def test_bluray_detail_view_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("blurays:blurays_detail", kwargs={"pk": self.bluray.pk,
                                                        "slug": self.bluray.slug})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blurays/blurays_detail.html")
        self.assertIn("PROFIL", response.content.decode())
        self.assertIn(self.bluray.title, response.content.decode())
