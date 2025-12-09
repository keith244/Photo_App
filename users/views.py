from django.shortcuts import render,redirect, get_object_or_404
from.models import User , Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError


# Create your views here.
def iregister(request):

    context = {
        'username': '',
        'email' : '',
        'password' : '',
        'password2': '',
    }

    if request.method == 'POST':
        context['username']  = request.POST.get('username')
        context['email'] = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        """This part ensures that the passwords provided match"""
        if password != password2:
            messages.error(request, f'The passwords don\'t match.')
            return render(request, 'users/register.html')
        
        """Why?This part ensures email is unique"""
        if User.objects.filter(email = context['email']).exists():
            messages.error (request, f'A user with that email already exists')
            return render(request, 'users/register.html')
        
        """Username should also be unique"""
        if User.objects.filter(username = context['username']).exists():
            messages.error(request, f'The username: <strong>{context['username']}</strong> is already taken.')
            return render(request, 'users/register.html')
        
        """To create the user if all above are okay"""
        user = User.objects.create(
            username = context['username'],
            email = context['email'],
        )

        user.set_password(password)
        user.is_active = True
        user.save()
        messages.success(request, f'Account created successfully for <strong>{context['username']}</strong>.Please log in.')
        return redirect('login')

    return render(request, 'users/register.html', context)

def ilogin(request):

    context = {
        'username': '',
    }

    if request.method == 'POST':
        context['username'] = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate ( request, username=context['username'], password=password)

        if user is not None:
            login(request,user)
            messages.success(request, f'Welcome, {context['username']}!')
            return redirect('index')
        else:
            if User.objects.filter(username=context['username']).exists():
                messages.error(request, 'Invalid credentials provided.')
            else:
                messages.error(request, f'Account with the username <strong>{context['username']}</strong> does not exist.')
            return redirect('login')
        
    return render(request, 'users/login.html',context)

def ilogout(request):
    logout(request)
    return redirect('login')

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
