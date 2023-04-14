from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import register, profile
from django.contrib.auth import views as auth_views


class TestUrls(SimpleTestCase):
    
    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)
    
    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_password_reset_url(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url(self):
        uidb64 = 'MQ'
        token = '463-9c763d2080d01c09b85c'
        url = reverse('password_reset_confirm', args=[uidb64, token])
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    