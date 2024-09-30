from flask import Flask, render_template, request, redirect, flash
from mastodon import Mastodon
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Initialize Mastodon API with your access token
mastodon = Mastodon(
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url=os.getenv('MASTODON_API_BASE_URL')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    content = request.form['content']
    if content:  # Check if content is not empty
        try:
            post = mastodon.status_post(content)
            post_id = post['id']  # Get the ID of the newly created post
            flash(f'Post created successfully! Post ID: {post_id}')
        except Exception as e:
            flash(f'Error creating post: {e}')
    else:
        flash('Content cannot be blank.')
    return redirect('/')

@app.route('/retrieve', methods=['GET'])
def retrieve():
    post_id = request.args.get('post_id')  # Get post_id from the query parameter
    if post_id:
        try:
            post = mastodon.status(post_id)
            return f"Post Content: {post['content']}"
        except Exception as e:
            return f"Error retrieving post: {e}"
    return "Post ID is required."

@app.route('/delete', methods=['POST'])
def delete():
    post_id = request.form['post_id']  # Get post_id from the form
    print(f"Attempting to delete post with ID: {post_id}")  # Debugging line
    if post_id:
        try:
            mastodon.status_delete(post_id)
            flash('Post deleted successfully!')
        except Exception as e:
            flash(f'Error deleting post: {e}')  # General error handling
    else:
        flash('Post ID is required.')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
