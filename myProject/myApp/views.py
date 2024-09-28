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
from .models import Category

@login_required
def Template1CreateView(request):
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES)  # Handle form submission
        if form.is_valid():
            aboutme = form.save(commit=False)  # Create the object but don't save yet
            aboutme.user = request.user  # Assign the logged-in user to the object

            # Set the category to "Template1"
            template1_category = Category.objects.get(type='template1')
            aboutme.category = template1_category  # Assign the category

            aboutme.save()  # Save the object
            return redirect('main')  # Redirect to the desired page after saving
    else:
        form = AboutMeForm()  # Create a new form instance for GET requests

    return render(request, 'myApp/template1.html', {'form': form})  # Render the te Render the template with the form


@login_required
def Template1EditView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES, instance=about_me)
        if form.is_valid():
            form.save()
            return redirect('template_list')
    else:
        form = AboutMeForm(instance=about_me)

    return render(request, 'myApp/edit_template1.html', {'form': form})

@login_required
def Template1DeleteView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        about_me.delete()
        return redirect('main')

    return render(request, 'myApp/savedTemplate1.html', {'about_me': about_me})


# views.py
# views.py
from django.shortcuts import render
from .models import AboutMe

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import AboutMe
def template1_list(request):
    # Filter profiles by the logged-in user and the specified category
    template1_category = Category.objects.get(type='template1')
    about_me_profiles = AboutMe.objects.filter(user=request.user, category=template1_category)
    print(about_me_profiles)  # Check the filtered profiles in your console

    return render(request, 'myApp/savedTemplate1.html', {
        'templates': about_me_profiles
    })


@login_required
def Template2CreateView(request):
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES)  # Handle form submission
        if form.is_valid():
            Aboutme = form.save(commit=False)  # Create the object but don't save yet
            Aboutme.user = request.user  # Assign the logged-in user to the object
            Aboutme.save()  # Save the object
            return redirect('main')  # Redirect to the desired page after saving
    else:
        form = AboutMeForm()  # Create a new form instance for GET requests

    return render(request, 'myApp/temp2/template2.html', {'form': form})

@login_required
def template2_list(request):
    about_me_profiles = AboutMe.objects.filter(user=request.user)
    print(about_me_profiles)  # Check the filtered profiles in your console

    return render(request, 'myApp/temp2/savedTemplate2.html', {
        'templates': about_me_profiles
    })




