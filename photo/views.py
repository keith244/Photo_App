from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

def index(request):
    posts = Post.objects.all().order_by('-date_created')
    p = Paginator(posts, 5) 
    context = {
        'posts': posts
    }
    return render(request, 'photo/index.html',context)

@login_required(login_url='login')
def create_post(request):
    context = {
        'title': '',
        'about': '',
        'category': '',
        'user_posts': Post.objects.filter(user=request.user).order_by('-date_created')
    }
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        about = request.POST.get('about')
        category = request.POST.get('category')

        context.update({
            'title': title,
            'about': about,
            'category': category
        })

        if not image:
            messages.error(request, 'Please upload an image')
        else:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
            validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
            try:
                validator(image)
            except ValidationError:
                messages.error(request, 'Invalid file type. Please upload a JPG, JPEG, PNG or GIF.')
            else:
                if all([image, title, about, category]):
                    Post.objects.create(
                        user=request.user,
                        image=image,
                        title=title,
                        about=about,
                        category=category,
                    )
                    messages.success(request, 'Post created successfully')
                    return redirect('index')
                # else:
                #     messages.error(request, 'Please fill all required fields.')

    return render(request, 'photo/upload_photo.html', context)

def post_details(request, post_id):
    post = get_object_or_404 (Post, id= post_id)
    referer = request.META.get('HTTP_REFERER', request.build_absolute_uri(reverse('index')))
    context = {
        'post':post,
        'referer':referer,
    }
    return render(request, 'photo/post_details.html',context)

@login_required(login_url='login')
def update_post(request, post_id):
    post = get_object_or_404(Post,pk = post_id )
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        about = request.POST.get('about')
        category = request.POST.get('category')
        if image:
            post.image = image
        post.title = title
        post.about = about
        post.category = category

        post.save()

        messages.success(request, 'Post update success')
        return redirect('index')

    return render(request, 'photo/update_post.html',{'post':post})

@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('index')  # or wherever you want to redirect after deletion
    
    return render(request, 'photo/delete_post.html', {'post': post})

def user_posts(request,username):
    user = get_object_or_404(User, username= username)
    posts = Post.objects.filter(user=user).order_by('-date_created')
    context = {
        'user':user,
        'posts':posts
    }
    return render(request, 'photo/user-posts.html', context)