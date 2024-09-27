from django.shortcuts import render

# Create your views here.
def home(request):
    context={}
    return render(request,'myApp/home.html',context)



def profile(request):
    context={}
    return render(request,'myApp/profile.html',context)

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



from django.shortcuts import render, redirect
from .forms import PortfolioForm, PortfolioElementForm
from .models import Portfolio

from django.shortcuts import render, redirect
from .forms import PortfolioForm  # Ensure PortfolioForm has an ImageField
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user  # Set the user to the currently logged-in user
            portfolio.save()
            return redirect('portfolio_list')  # Redirect to the portfolio list page
    else:
        form = PortfolioForm()

    return render(request, 'myApp/create_portfolio.html', {'form': form})

def edit_portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('portfolio_list')
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'myApp/edit_portfolio.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Portfolio

@login_required
def portfolio_list(request):
    # Get portfolios associated with the logged-in user
    portfolios = Portfolio.objects.filter(user=request.user)
    about_me_profiles = AboutMe.objects.all()  

    return render(request, 'myApp/portfolio_list.html', {
        'portfolios': portfolios,
        'templates': about_me_profiles  # Pass the profiles as templates
    })




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio

@login_required
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)

    if request.method == 'POST':
        portfolio.delete()
        return redirect('portfolio_list')  # Redirect to the portfolio list after deletion

    return render(request, 'myApp/delete_portfolio.html', {'portfolio': portfolio})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

@csrf_exempt  # Remove in production and use CSRF tokens
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        uploaded_file = request.FILES['upload']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        return JsonResponse({'uploaded': True, 'url': file_url})
    return JsonResponse({'uploaded': False, 'error': 'File upload failed.'})





from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AboutMe
from .forms import AboutMeForm  # Make sure to create this form



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AboutMeForm  # Ensure you have imported your form
from .models import AboutMe

@login_required
def AboutMeCreateView(request):
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES)
        if form.is_valid():
            Aboutme = form.save(commit=False)
            Aboutme.user = request.user  # Set user to the logged-in user
            Aboutme.save()
            return redirect('main')  # Redirect to the desired page after saving
    else:
        form = AboutMeForm()

    return render(request, 'myApp/template1.html', {'form': form})



@login_required
def aboutme_list(request):
    # Get portfolios associated with the logged-in user
    aboutme = aboutme.objects.filter(user=request.user)

    return render(request, 'myApp/portfolio_list.html', {'about_me': aboutme})


# views.py
# views.py
from django.shortcuts import render
from .models import AboutMe

def about_me_list(request):
    about_me_profiles = AboutMe.objects.all()
    return render(request, 'myApp/savedTemplates.html',  {'templates': about_me_profiles})







