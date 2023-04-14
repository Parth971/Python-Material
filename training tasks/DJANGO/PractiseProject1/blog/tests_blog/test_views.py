from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testuser123'
        self.user = User.objects.create_user(self.username, 'testuser@company.com', self.password)
        self.post1 = Post.objects.create(
            title='test title 1',
            content='test content 1',
            author=self.user
        )
        self.post2 = Post.objects.create(
            title='test title 2',
            content='test content 2',
            author=self.user
        )
        self.blog_home_url = reverse('blog-home')
        self.user_post_url = reverse('user-post', args=[self.username])
        self.post_detail_url = reverse('post-detail', args=[self.post1.id])
        self.post_update_url = reverse('post-update', args=[self.post1.id])
        self.post_delete_url = reverse('post-delete', args=[self.post1.id])
        self.post_create_url = reverse('post-create')
        self.blog_about_url = reverse('blog-about')
        self.login_url = reverse('login')

    # GET TESTS
    def test_blog_home_GET(self):
        response = self.client.get(self.blog_home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_user_post_GET(self):
        response = self.client.get(self.user_post_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.user.post_set.count(), 2)
        self.assertTemplateUsed(response, 'blog/user_posts.html')

    def test_post_detail_GET(self):
        response = self.client.get(self.post_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_update_without_login_GET(self):
        response = self.client.get(self.post_update_url)
        
        expected_url = self.login_url + '?next=' + self.post_update_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)
    
    def test_post_update_with_login_with_correct_user_GET(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)
        
        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.post_update_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_update_with_login_with_incorrect_user_GET(self):
        User.objects.create_user('dummyuser', 'dummyuser@company.com', 'dummyuser@123')
        self.logged_in = self.client.login(username='dummyuser', password='dummyuser@123')
        
        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.post_update_url)
        
        self.assertEquals(response.status_code, 403)
        
    def test_post_delete_without_login_GET(self):
        response = self.client.get(self.post_delete_url)

        expected_url = self.login_url + '?next=' + self.post_delete_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_post_delete_with_login_with_correct_user_GET(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)
        
        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.post_delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_post_delete_with_login_with_incorrect_user_GET(self):
        User.objects.create_user('dummyuser', 'dummyuser@company.com', 'dummyuser@123')
        self.logged_in = self.client.login(username='dummyuser', password='dummyuser@123')
        
        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.post_delete_url)

        self.assertEquals(response.status_code, 403)

    def test_post_create_with_login_GET(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)
        
        self.assertEquals(self.logged_in, True)

        response = self.client.get(self.post_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_create_without_login_GET(self):
        response = self.client.get(self.post_create_url)

        expected_url = self.login_url + '?next=' + self.post_create_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_blog_about_GET(self):
        response = self.client.get(self.blog_about_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')


    # POST TESTS
    def test_post_create_with_login_with_data_POST(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)

        response = self.client.post(self.post_create_url, data={
            'title': 'Post title',
            'content': 'Post Content'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.user.post_set.count(), 3)

    def test_post_create_with_login_without_data_POST(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)

        response = self.client.post(self.post_create_url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
        self.assertEquals(self.user.post_set.count(), 2)

    def test_post_create_without_login_POST(self):
        response = self.client.post(self.post_create_url)

        expected_url = self.login_url + '?next=' + self.post_create_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_post_update_without_login_POST(self):
        response = self.client.post(self.post_update_url)

        expected_url = self.login_url + '?next=' + self.post_update_url
        self.assertRedirects(response, expected_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_post_update_with_login_without_data_POST(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)

        response = self.client.post(self.post_update_url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_update_with_login_with_data_with_correct_user_POST(self):
        self.logged_in = self.client.login(username=self.username, password=self.password)

        response = self.client.post(self.post_update_url, data={
            'title': 'Updated Post',
            'content': 'Updated Post Content'
        })

        self.assertEquals(self.user.post_set.count(), 2)
        self.assertRedirects(response, self.post_detail_url, status_code=302,
                        target_status_code=200, msg_prefix='',
                        fetch_redirect_response=True)

    def test_post_update_with_login_with_data_with_incorrect_user_POST(self):
        User.objects.create_user('dummyuser', 'dummyuser@company.com', 'dummyuser@123')
        self.logged_in = self.client.login(username='dummyuser', password='dummyuser@123')
        
        self.assertEquals(self.logged_in, True)

        response = self.client.post(self.post_update_url, data={
            'title': 'Updated Post',
            'content': 'Updated Post Content'
        })

        self.assertEquals(response.status_code, 403)