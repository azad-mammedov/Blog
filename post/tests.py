from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from post.models import Post

class PostViewTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.other_user = CustomUser.objects.create_user(username='otheruser', password='password')

        # Create a post for testing
        self.post = Post.objects.create(title='Test Post', content='Test Content', created_by=self.user)

    def test_post_create_view_get(self):
        # Test accessing the post creation page as a logged-in user
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_create.html')

    def test_post_create_view_post(self):
        # Test creating a new post as a logged-in user
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_create'), {'title': 'New Post', 'content': 'New Content'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful post creation
        self.assertTrue(Post.objects.filter(title='New Post').exists())
        self.assertRedirects(response, reverse('index'))

    def test_post_detail_view_get(self):
        # Test accessing the post detail view
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_post_detail_view_post(self):
        # Test updating a post as the author
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.post.pk]), {'title': 'Updated Title', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated Content')
        self.assertRedirects(response, reverse('post_detail', args=[self.post.pk]))

    def test_post_detail_view_post_not_author(self):
        # Test updating a post as a different user (should be forbidden)
        self.client.login(username='otheruser', password='password')
        response = self.client.post(reverse('post_detail', args=[self.post.pk]), {'title': 'Should Not Update', 'content': 'Should Not Update'})
        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_get(self):
        # Test accessing the post delete confirmation page
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_confirm_delete.html')

    def test_post_delete_view_post(self):
        # Test deleting a post as the author
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        self.assertRedirects(response, reverse('index'))

    def test_post_delete_view_post_not_author(self):
        # Test deleting a post as a different user (should be forbidden)
        self.client.login(username='otheruser', password='password')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

