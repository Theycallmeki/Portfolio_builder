from django.shortcuts import render

# Create your views here.
def home(request):
    context={}
    return render(request,'myApp/home.html',context)

def contact(request):
    context={}

    return render(request, 'components/contact.html')
def main(request):
    context={}

    return render(request, 'myApp/main.html', context)

def create(request):
    context={}

    return render(request, 'myApp/create.html')

def navbar(request):
    context={}

    return render(request, 'components/navbar.html')

    



from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to a home page after registration
    else:
        form = RegistrationForm()
    return render(request, 'myApp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')  # Redirect to a home page after login
    else:
        form = LoginForm()
    return render(request, 'myApp/login.html', {'form': form})

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('home') 

