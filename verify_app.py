import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotrix.settings')
import sys
print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")
try:
    django.setup()
except Exception as e:
    print(f"Setup Error: {e}")
    sys.exit(1)

from django.test import Client
from blog.models import BlogPost

def run_verification():
    print("Starting Verification...")
    client = Client()

    # 1. Test Model Creation
    post_count_start = BlogPost.objects.count()
    print(f"Initial Post Count: {post_count_start}")

    # 2. Test Create View (POST) with WRONG password
    response = client.post('/create/', {'title': 'Fail', 'content': 'Fail', 'password': 'WrongPassword'})
    if BlogPost.objects.count() == post_count_start:
        print("PASS: Post NOT created with wrong password.")
    else:
        print("FAIL: Post created with wrong password.")

    # 3. Test Create View (POST) with CORRECT password
    response = client.post('/create/', {'title': 'UI Post', 'content': 'Created via UI', 'password': 'Emotrix1$'}, follow=True)
    if BlogPost.objects.count() == post_count_start + 1:
        print("PASS: Post created with correct password.")
    else:
        print("FAIL:  Post NOT created with correct password.")
    ##ff

    # 4. Test Home View
    response = client.get('/')
    if response.status_code == 200 and 'UI Post' in response.content.decode():
        print("PASS: Home view returns 200 and contains post title.")
    else:
        print(f"FAIL: Home view status {response.status_code}")

    # 5. Test API Create (No Auth)
    data = {'title': 'API Post', 'content': 'Created via API'}
    response = client.post('/api/posts/create/', data, content_type='application/json')
    if response.status_code == 201:
        print("PASS: API Create returned 201.")
    else:
        print(f"FAIL: API Create returned {response.status_code} - {response.content}")
    
    # 6. Test API List
    response = client.get('/api/posts/')
    if response.status_code == 200:
        json_data = response.json()
        if len(json_data['posts']) >= 2:
            print("PASS: API List returned posts.")
        else:
            print("FAIL: API List returned insufficient posts.")
    else:
        print(f"FAIL: API List returned {response.status_code}")

    # 7. Test API Detail
    post_id = BlogPost.objects.last().id
    response = client.get(f'/api/posts/{post_id}/')
    if response.status_code == 200:
        print("PASS: API Detail returned 200.")
    else:
        print(f"FAIL: API Detail returned {response.status_code}")

if __name__ == '__main__':
    run_verification()
