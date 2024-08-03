from django.shortcuts import render,redirect
from.models import User 
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
# Create your views here.
def iregister(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        """This part ensures that the passwords provided match"""
        if password != password2:
            messages.error(request, f'The passwords don\'t match.')
            return render(request, 'users/register.html')
        
        """Why?This part ensures email is unique"""
        if User.objects.filter(email=email).exists():
            messages.error (request, f'A user with that email already exists')
            return render(request, 'users/register.html')
        
        """Username should also be unique"""
        if User.objects.filter(username = username).exists():
            messages.error(request, f'The username: <strong>{username}</strong> is already taken.')
            return render(request, 'users/register.html')
        
        """To create the user if all above are okay"""
        user = User.objects.create(
            username = username,
            email = email,
        )

        user.set_password(password)
        user.is_active = True
        user.save()
        messages.success(request, f'Account created successfully for <strong>{username}</strong>.Please log in.')
        return redirect('login')

    return render(request, 'users/register.html')

def ilogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate ( request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('index')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid credentials provided.')
            else:
                messages.error(request, f'Account with the username <strong>{username}</strong> does not exist.')
            return redirect('login')
        
    return render(request, 'users/login.html')

def ilogout(request):
    logout(request)
    return redirect('login')
