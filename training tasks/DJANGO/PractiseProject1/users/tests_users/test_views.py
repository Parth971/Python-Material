from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')
        self.login_url = reverse('login')
    
    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_profile_without_login_GET(self):
        response = self.client.get(self.profile_url)
        
        expected_url = self.login_url + '?next=' + self.profile_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_profile_with_login_GET(self):
        user = User.objects.create_user('testuser', 'testuser@company.com', 'testuser123')
        
        self.logged_in = self.client.login(username='testuser', password='testuser123')
        
        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_register_POST(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser1',
            'email': 'testuser1@company.com',
            'password1': 'username123',
            'password2': 'username123',
        })
        
        self.assertRedirects(response, self.login_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_profile_without_login_POST(self):
        response = self.client.post(self.profile_url)

        expected_url = self.login_url + '?next=' + self.profile_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)
        
    def test_profile_with_login_with_data_POST(self):
        user = User.objects.create_user('testuser', 'testuser@company.com', 'testuser123')
        
        self.logged_in = self.client.login(username='testuser', password='testuser123')
        
        self.assertEquals(self.logged_in, True)

        response = self.client.post(self.profile_url, {
            'username': 'updatedUsername',
            'email': 'updatedUsername@company.com',
        })

        self.assertRedirects(response, self.profile_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_profile_with_login_without_data_POST(self):
        user = User.objects.create_user('testuser', 'testuser@company.com', 'testuser123')
        
        self.logged_in = self.client.login(username='testuser', password='testuser123')
        
        self.assertEquals(self.logged_in, True)

        response = self.client.post(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')