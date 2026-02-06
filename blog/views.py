from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
import json
from .models import BlogPost

def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'detail.html', {'post': post})

def create_post(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == "Emotrix1$":
            title = request.POST.get('title')
            content = request.POST.get('content')
            BlogPost.objects.create(title=title, content=content)
            messages.success(request, 'Blog post created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Password!')
            return render(request, 'create.html', {'error': 'Incorrect Password'})
            return render(request, 'create.html', {'error': 'Incorrect Password'})
    return render(request, 'create.html')

def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == "Emotrix1$":
            post.delete()
            messages.success(request, 'Blog post deleted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Password!')
            return render(request, 'delete.html', {'post': post, 'error': 'Incorrect Password'})
    return render(request, 'delete.html', {'post': post})

# API Views

def api_get_blogs(request):
    # GET API to list all blog posts
    posts = BlogPost.objects.all().order_by('-created_at')
    data = {"posts": list(posts.values('id', 'title', 'content', 'author', 'created_at'))}
    return JsonResponse(data)

def api_get_post_detail(request, post_id):
    # GET API to get a single post
    try:
        post = BlogPost.objects.get(id=post_id)
        data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'created_at': post.created_at
        }
        return JsonResponse(data)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@csrf_exempt
def api_create_post(request):
    # POST API to create a blog post (No authentication required as requested)
    if request.method == 'POST':
        try:
            # Try parsing JSON body first
            try:
                data = json.loads(request.body)
                title = data.get('title')
                content = data.get('content')
            except json.JSONDecodeError:
                # If not JSON, try creating from form data if needed, but API usually implies JSON.
                # Let's support form data too just in case.
                title = request.POST.get('title')
                content = request.POST.get('content')

            if not title or not content:
                return JsonResponse({'error': 'Title and Content are required'}, status=400)

            post = BlogPost.objects.create(title=title, content=content)
            return JsonResponse({
                'message': 'Blog post created successfully',
                'id': post.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def api_docs_view(request):
    return render(request, 'docs.html')
