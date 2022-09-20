from django.test import TestCase

from django.contrib.auth.models import User

from budget_app.models import Profile


class ProfileTestCase(TestCase):
    urls = 'VendingMachine.vending_app.urls'

    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user', password='test_password', email='t@t.pl')

    def test_is_profile_created(self):
        ret = Profile.objects.get(user=self.test_user)
        self.assertIsNotNone(ret)
        self.assertEqual(ret.user, self.test_user)
