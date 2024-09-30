from mastodon import Mastodon
import os

# Initialize the Mastodon client
class MastodonService:
    def __init__(self):
        self.mastodon = Mastodon(
            access_token=os.getenv('MASTODON_ACCESS_TOKEN'),  # Access token from environment variable
            api_base_url=os.getenv('MASTODON_API_BASE_URL')   # API base URL from environment variable
        )

    # Function to create a post (status update)
    def create_post(self, status_message):
        try:
            post = self.mastodon.status_post(status_message)
            return post
        except Exception as e:
            print(f"Error creating post: {e}")
            return None

    # Function to retrieve a post by ID
    def retrieve_post(self, post_id):
        try:
            post = self.mastodon.status(post_id)
            return post
        except Exception as e:
            print(f"Error retrieving post: {e}")
            return None

    # Function to delete a post by ID
    def delete_post(self, post_id):
        try:
            self.mastodon.status_delete(post_id)
            return True
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False
