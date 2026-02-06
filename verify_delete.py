import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotrix.settings')
try:
    django.setup()
except Exception as e:
    print(f"Setup Error: {e}")
    sys.exit(1)

from django.test import Client
from blog.models import BlogPost

def run_verification():
    print("Starting Delete Verification...")
    client = Client()

    # Create dummy post
    post = BlogPost.objects.create(title="Delete Me", content="To be deleted.")
    post_id = post.id
    print(f"Created dummy post: {post_id}")

    # 1. Try deleting with WRONG password
    response = client.post(f'/post/{post_id}/delete/', {'password': 'WrongPassword'})
    if BlogPost.objects.filter(id=post_id).exists():
        print("PASS: Post NOT deleted with wrong password.")
    else:
        print("FAIL: Post deleted with wrong password.")

    # 2. Try deleting with CORRECT password
    response = client.post(f'/post/{post_id}/delete/', {'password': 'Emotrix1$'}, follow=True)
    if not BlogPost.objects.filter(id=post_id).exists():
        print("PASS: Post deleted with correct password.")
    else:
        print("FAIL: Post NOT deleted with correct password.")

if __name__ == '__main__':
    run_verification()
