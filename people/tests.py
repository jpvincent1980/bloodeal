# from django.test import TestCase
# from django.urls import reverse
#
# from accounts.models import CustomUser
# from people.models import People
#
#
# # Create your tests here.
# class PeopleTest(TestCase):
#     def setUp(self) -> None:
#         self.user = CustomUser.objects.create(email="test@gmail.com")
#         self.user.set_password("azerty01")
#         self.user.save()
#         self.people = People.objects.create(first_name="Denis",
#                                             last_name="Villeneuve")
#
#     def test_people_list_view_anonymous_user(self):
#         url = reverse("people:people_list")
#         response = self.client.get(url)
#         self.failUnlessEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "people/people_list.html")
#         self.assertNotIn("PROFIL", response.content.decode())
#         self.assertIn(self.people.first_name, response.content.decode())
#         self.assertIn(self.people.last_name, response.content.decode())
#
#     def test_people_list_view_authenticated_user(self):
#         self.client.login(email="test@gmail.com",
#                           password="azerty01")
#         url = reverse("people:people_list")
#         response = self.client.get(url)
#         self.failUnlessEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "people/people_list.html")
#         self.assertIn("PROFIL", response.content.decode())
#         self.assertIn(self.people.first_name, response.content.decode())
#         self.assertIn(self.people.last_name, response.content.decode())
