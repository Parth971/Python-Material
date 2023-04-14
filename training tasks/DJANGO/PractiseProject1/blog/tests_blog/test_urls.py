from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import PostListView, UserPostListView, PostDetailView, PostUpdateView, PostDeleteView, PostCreateView, about


class TestUrls(SimpleTestCase):
    
    def test_blog_home_url(self):
        url = reverse('blog-home')
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_user_post_url(self):
        username = 'parth'
        url = reverse('user-post', args=[username])
        self.assertEquals(resolve(url).func.view_class, UserPostListView)

    def test_post_detail_url(self):
        pk = 1
        url = reverse('post-detail', args=[pk])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_post_update_url(self):
        pk = 1
        url = reverse('post-update', args=[pk])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_post_delete_url(self):
        pk = 1
        url = reverse('post-delete', args=[pk])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)

    def test_post_create_url(self):
        url = reverse('post-create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_about_url(self):
        url = reverse('blog-about')
        self.assertEquals(resolve(url).func, about)