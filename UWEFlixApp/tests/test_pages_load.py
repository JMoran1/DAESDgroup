from django.test import TestCase
from django.urls import reverse
from UWEFlixApp.models import MonthlyStatement, Club

class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

class ViewMonthlyStatementTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/view_monthly_statement/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("view_monthly_statement"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("view_monthly_statement"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "UWEFlixApp/view_monthly_statement.html")

class CreateClubTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/create_club/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("create_club"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("create_club"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "UWEFlixApp/create_club_form.html")

    @classmethod
    def setUpTestData(cls):
        cls.post = Club.objects.create(name="UWEFlix", card_number="123456", card_expiry="2020-12-31", discount_rate=0.1, address="Bristol")
    
    def test_model_content(self):
        self.assertEqual(self.post.name, "UWEFlix")
        self.assertEqual(self.post.card_number, "123456")
        self.assertEqual(self.post.card_expiry, "2020-12-31")
        self.assertEqual(self.post.discount_rate, 0.1)
        self.assertEqual(self.post.address, "Bristol")
