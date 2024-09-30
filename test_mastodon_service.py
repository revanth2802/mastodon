import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestMastodonAPIIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.mastodon.status_post')
    def test_create_post_success(self, mock_status_post):
        mock_status_post.return_value = {'id': 12345}
        response = self.app.post('/create', data={'content': 'Hello, World!'})
        self.assertEqual(response.status_code, 302)
        with self.app.session_transaction() as session:
            self.assertIn(('message', 'Post created successfully! Post ID: 12345'), session['_flashes'])

    @patch('app.mastodon.status')
    def test_retrieve_post_success(self, mock_status):
        mock_status.return_value = {'content': 'Hello, World!', 'id': 12345}
        response = self.app.get('/retrieve?post_id=12345')
        self.assertIn(b"Post Content: Hello, World!", response.data)

    @patch('app.mastodon.status_delete')
    def test_delete_post_success(self, mock_status_delete):
        mock_status_delete.return_value = None
        response = self.app.post('/delete', data={'post_id': 12345})
        self.assertEqual(response.status_code, 302)
        with self.app.session_transaction() as session:
            self.assertIn(('message', 'Post deleted successfully!'), session['_flashes'])

    @patch('app.mastodon.status_delete')
    def test_delete_post_failure(self, mock_status_delete):
        mock_status_delete.side_effect = Exception('Failed to delete post.')
        response = self.app.post('/delete', data={'post_id': 12345})
        self.assertEqual(response.status_code, 302)
        with self.app.session_transaction() as session:
            self.assertIn(('message', 'Error deleting post: Failed to delete post.'), session['_flashes'])

if __name__ == '__main__':
    unittest.main()
