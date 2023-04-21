from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Club, MonthlyStatement, Movie, Screen, Screening, User

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
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.ACCOUNT_MANAGER)
        self.client.force_login(self.user)

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

    def tearDown(self):
        self.user.delete()

class CreateMonthlyStatementTest(TestCase):
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.ACCOUNT_MANAGER)
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/create_monthly_statement')
        self.assertEqual(response.status_code, 301)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("create_monthly_statement"))
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.user.delete()

class ViewClubsTest(TestCase):
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.ACCOUNT_MANAGER)
        self.client.force_login(self.user)

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

    def tearDown(self):
        self.user.delete()

class UpdateClubTest(TestCase):
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.ACCOUNT_MANAGER)
        self.client.force_login(self.user)

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

    def tearDown(self):
        self.user.delete()

class DeleteClubTest(TestCase):
    def setUp(self):
        self.user = create_test_user_of_role(User.Role.ACCOUNT_MANAGER)
        self.client.force_login(self.user)
    
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

    def tearDown(self):
        self.user.delete()

class ClashingScreeningsTest(TestCase):
    """
    Successfully detecting all the possible situations in which two events may
    overlap is tricky as the "orientation" of said overlaps can be in one of
    many different possible configurations. Test them all to make sure we have
    full coverage!
    """
    @staticmethod
    def make_screenings_for_date_ranges(
        a: tuple[str, str], b: tuple[str, str]
    ):
        """
        Helper method, will produce two Screenings for the same Screen which are
        guaranteed to start and end at the given tuples of (start, end) times.

        NOTE: pass datetimes in as ISO-8601 string, because making datetime
        objects is faffy.

        Screenings aren't saved, but returned as objects that can then be saved
        to the db if desired.
        """
        überskrün = Screen.objects.create(name='DAS ÜBERSKRÜN', capacity=9001)
        a_start = datetime.fromisoformat(a[0])
        a_end = datetime.fromisoformat(a[1])
        b_start = datetime.fromisoformat(b[0])
        b_end = datetime.fromisoformat(b[1])
        a_screening = Screening(
            screen=überskrün,
            showing_at=a_start,
            movie=Movie.objects.create(
                name='Bandusshels die Wudhandlen',
                running_time=(a_end - a_start)
            )
        )
        b_screening = Screening(
            screen=überskrün,
            showing_at=b_start,
            movie=Movie.objects.create(
                name='Der Whuffen der Neaph?',
                running_time=(b_end - b_start)
            )
        )
        return a_screening, b_screening

    def test_non_clashing_screenings(self):
        """
        It should be possible to create two Screenings for the same Screen that
        do not clash, without an error. We should be able to create block
        bookings (i.e. a Screening that starts at precisely the time that the
        one before it ended) without issue.
        """
        start = '2029-08-07T12:52'
        middle = '2029-08-07T14:19'
        end = '2029-08-07T18:54'
        first, second = self.make_screenings_for_date_ranges(
            (start, middle),
            (middle, end)
        )

        first.save()
        second.save()

    def test_coincident_screenings(self):
        """
        coincident: like two lines which happen to be exactly the same, i.e. two
        Screenings that start and end at the exact same time.
        """
        start = '2011-12-12T13:33'
        end = '2011-12-12T14:52'
        a, b = self.make_screenings_for_date_ranges((start, end), (start, end))

        # GIVEN an existing Screening with this start and end times
        a.save()

        # WHEN another with identical start and end times is attempted to be created
        with self.assertRaises(ValidationError):
            # THEN an error is raised
            b.save()

    def tearDown(self):
        """
        Delete anything we might have inadvertently created
        """
        for model in (Screening, Screen, Movie):  # delete in correct order for db constraints
            model.objects.all().delete()
