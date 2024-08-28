from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Paginator

from users.models import CustomUser
from post.models import Post

class IndexViewTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create_user(username='testuser', password='password')

        # Create multiple posts for pagination testing
        for i in range(10):
            Post.objects.create(title=f'Test Post {i+1}', content='Test Content', created_by=self.user)

    def test_index_view_status_code(self):
        # Test the index view returns a 200 status code
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        # Test the index view uses the correct template
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_context_data(self):
        # Test the index view provides correct context data
        response = self.client.get(reverse('index'))
        self.assertIn('blogs', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['blogs']), 10)

    def test_index_view_pagination(self):
        # Test pagination: should show 3 posts per page
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context['page_obj'].object_list), 3)
        self.assertTrue(response.context['page_obj'].has_next())

        # Test the second page
        response = self.client.get(reverse('index'), {'page': 2})
        self.assertEqual(len(response.context['page_obj'].object_list), 3)
        self.assertTrue(response.context['page_obj'].has_next())

        # Test the last page
        response = self.client.get(reverse('index'), {'page': 4})
        self.assertEqual(len(response.context['page_obj'].object_list), 1)
        self.assertFalse(response.context['page_obj'].has_next())

    def test_index_view_invalid_page(self):
        # Test invalid page number, should default to the first page
        response = self.client.get(reverse('index'), {'page': 'invalid'})
        self.assertEqual(len(response.context['page_obj'].object_list), 3)
        self.assertTrue(response.context['page_obj'].has_next())
