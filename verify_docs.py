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
    print("Starting Verification...")
    client = Client()

    # 1. Test Docs Page
    try:
        response = client.get('/docs/')
        if response.status_code == 200:
            content = response.content.decode()
            if '<h1 class="text-3xl font-bold mb-4">Emotrix Blog API Documentation</h1>' in content:
                print("PASS: Docs page is 200 and contains correct HTML title.")
            else:
                print("FAIL: Docs page found but HTML content mismatch.")
        else:
            print(f"FAIL: Docs page status {response.status_code}")
    except Exception as e:
        print(f"FAIL: Error accessing docs page - {e}")

if __name__ == '__main__':
    run_verification()
