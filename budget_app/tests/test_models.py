from django.test import TestCase

from django.contrib.auth.models import User

from django.test.client import RequestFactory

from django.contrib.auth.models import AnonymousUser

from budget_app import views
from budget_app.tests.utils import BudgetTestCase

class TestTeamsView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test1',
            email='abc1@gmail.com',
            first_name='t',
            last_name='u',
            password='password'
        )
    def test_team_list_view_with_valid_user(self):
        request = self.factory.get('/')
        request.user = self.user
        response = views.HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'budget_app/budget_list.html')
    
    def test_team_list_view_with_anonymous_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = views.HomeView.as_view()(request)
        self.assertEqual(response.status_code,302)
    def test_budget_update_view(self):
        pass
class TestModelsView(BudgetTestCase):

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
       
    def test_team_list_view_with_valid_user(self):
        request = self.factory.get('/')
        request.user = self.profiles[0].user
        response = views.HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'budget_app/budget_list.html')
    
    def test_team_list_view_with_anonymous_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = views.HomeView.as_view()(request)
        self.assertEqual(response.status_code,302)
    def test_budget_update_view(self):
        pass