from django.test import TestCase
from django.urls import reverse
from .models import MonthlyStatement, Club, User

class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

def create_test_user_of_role(role: User.Role):
    user = User.objects.create(username='winston', role=role)
    user.set_password('churchill')
    user.save()
    return user

class ViewMonthlyStatementTests(TestCase):
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.ACCOUNT_MANAGER)
        self.client.force_login(self.user)

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

    def tearDown(self):
        self.user.delete()

class CreateClubTests(TestCase):
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.CINEMA_MANAGER)
        self.client.force_login(self.user)

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

    def tearDown(self):
        self.user.delete()

class AccountManagerTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account_manager')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("account_manager"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("account_manager"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "UWEFlixApp/account_manager_page.html")

class CreateMonthlyStatementTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/create_monthly_statement')
        self.assertEqual(response.status_code, 301)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("create_monthly_statement"))
        self.assertEqual(response.status_code, 302)

class ViewClubsTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/view_clubs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("view_clubs"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("view_clubs"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "UWEFlixApp/view_clubs.html")

class UpdateClubTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/update_club/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("update_club", args=[1]))
        self.assertEqual(response.status_code, 200)

    @classmethod
    def setUpTestData(cls):
        cls.post = Club.objects.create(name="UWEFlix", card_number="123456", card_expiry="2020-12-31", discount_rate=0.1, address="Bristol")
    
    def test_model_content(self):
        self.assertEqual(self.post.name, "UWEFlix")
        self.assertEqual(self.post.card_number, "123456")
        self.assertEqual(self.post.card_expiry, "2020-12-31")
        self.assertEqual(self.post.discount_rate, 0.1)
        self.assertEqual(self.post.address, "Bristol")

class DeleteClubTest(TestCase):
    
        def test_view_url_exists_at_desired_location(self):
            response = self.client.get('/delete_club/1/')
            self.assertEqual(response.status_code, 302)
    
        def test_view_url_accessible_by_name(self):
            response = self.client.get(reverse("delete_club", args=[1]))
            self.assertEqual(response.status_code, 302)
        
        @classmethod
        def setUpTestData(cls):
            cls.post = Club.objects.create(name="UWEFlix", card_number="123456", card_expiry="2020-12-31", discount_rate=0.1, address="Bristol")
        
        def test_model_content(self):
            self.assertEqual(self.post.name, "UWEFlix")
            self.assertEqual(self.post.card_number, "123456")
            self.assertEqual(self.post.card_expiry, "2020-12-31")
            self.assertEqual(self.post.discount_rate, 0.1)
            self.assertEqual(self.post.address, "Bristol")