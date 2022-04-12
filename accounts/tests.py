from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


# Create your tests here.
class AccountsTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="test@gmail.com")
        self.user.set_password("azerty01")
        self.user.save()

    def test_index_anonymous_user(self):
        url = reverse("accounts:index")
        response = self.client.get(url)
        self.assertURLEqual(reverse("accounts:index"), "/")
        self.failUnlessEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("deals:deals_list"))
        response = self.client.get(url, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "deals/deals_list.html")
        self.assertNotIn("PROFIL", response.content.decode())

    def test_index_authenticated_user(self):
        self.client.login(email="test@gmail.com",
                          password="azerty01")
        url = reverse("accounts:index")
        response = self.client.get(url)
        self.assertURLEqual(reverse("accounts:index"), "/")
        self.failUnlessEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:dashboard"))
        response = self.client.get(url, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/dashboard.html")
        self.assertIn("PROFIL", response.content.decode())
