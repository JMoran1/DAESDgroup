from ddt import ddt, data
from django.test import TestCase
from UWEFlixApp.models import User  # TODO: replace with loading SETTINGS.AUTH_USER_MODEL

@ddt
class UserTestCase(TestCase):
    @data()
    @unpack
    def test_user_role():
        pass
