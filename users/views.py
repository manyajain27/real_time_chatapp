from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/chat/No User/')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    if request.user.is_authenticated:
        return redirect('/chat/No User/')
    
    return render(request, 'auth_form.html', {'form_type': 'login'})



@login_required
def logout_page(request):
    logout(request)  
    messages.success(request, 'You have been logged out successfully.') 
    return redirect('/')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password1 != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth_form.html', {'form_type': 'signup'})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'auth_form.html', {'form_type': 'signup'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('login')

    if request.user.is_authenticated:
        return redirect('/chat/No User/')
    
    return render(request, 'auth_form.html', {'form_type': 'signup'})
