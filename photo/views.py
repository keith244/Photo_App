from django.shortcuts import render, redirect, get_object_or_404
from .models import Post,Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()
def index(request):
    posts = Post.objects.all().order_by('-date_created')
    context = {
        'posts': posts
    }
    return render(request, 'photo/index.html',context)

@login_required(login_url='login')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST' and request.user == user:
        image = request.FILES.get('image')
        about = request.POST.get('about')
       
        try:
            if image:
                if image.size > 5 * 1024 * 1024:
                    raise ValidationError('Image too large (>5MB)')
                profile.image = image
            if about:
                if len(about) > 500:
                    raise ValidationError('The about is too long. About should be a maximum of 500 characters.')
                profile.about = about
            profile.full_clean()
            profile.save()
            if created:
                messages.success(request, f'Profile created successfully')
            else:
                messages.success(request, 'Profile updated successfully')
            return redirect('index')
        except ValidationError as e:
            messages.error(request, f'Validation error: {e}')
        except IntegrityError:
            messages.error(request, f'Error updating profile')
        except IOError:
            messages.error(request, f'Error handling uploaded file')

    return render(request, 'photo/profile.html', {'profile': profile, 'is_own_profile': request.user == user})


def profile_view(request,user_id):
    return render(request, 'photo/profile_view.html')


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        about = request.POST.get('about')
        category = request.POST.get('category')

        if not image:
            messages.error(request, f'Please upload an image')
            return render(request,'photo/upload_photo.html')
        
        allowed_extensions = ['jpg','jpeg','png','gif']
        validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
        try:
            validator(image)
        except ValidationError:
            messages.error(request, 'Invalid file type.Please upload a JPG,JPEG,PNG or GIF .')
            return render(request, 'photo/upload_photo.html')

        if all([image and title and about and category]):
            Post.objects.create(
                user = request.user,
                image = image,
                title = title,
                about = about,
                category= category,
            )
            messages.success(request, 'Post created successfully')
            return redirect('index')
        else:
            messages.error(request,'Please fill all required fields.')

    user_posts = Post.objects.filter(user= request.user).order_by('-date_created')
    return render(request, 'photo/upload_photo.html',{'user_posts':user_posts})

def post_details(request, post_id):
    post = get_object_or_404 (Post, id= post_id)
    return render(request, 'photo/post_details.html',{'post':post})

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
    post = get_object_or_404(Post, id = post_id, user= request.user)
    post.delete()
    return render(request,'photo/delete_post.html')