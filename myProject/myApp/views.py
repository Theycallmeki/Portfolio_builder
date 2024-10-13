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

def about(request):
    context={}

    return render(request, 'components/about.html')

def privacy_policy(request):
    context={}

    return render(request, 'components/privacy_policy.html')

def terms_and_conditions(request):
    context={}

    return render(request, 'components/terms_and_conditions.html')
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.urls import reverse

# Password Reset View (Handles both Request and Confirm)
def password_reset(request, uidb64=None, token=None):
    # Password Reset Request
    if uidb64 is None and token is None:
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                associated_users = User.objects.filter(email=email)
                if associated_users.exists():
                    for user in associated_users:
                        token = default_token_generator.make_token(user)
                        uidb64 = urlsafe_base64_encode(str(user.pk).encode())  # base64 encoding of the user ID
                        reset_url = request.build_absolute_uri(
                            reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                        )
                        # Send email to the user with the reset link
                        send_mail(
                            'Password Reset Request',
                            f'Click the following link to reset your password: {reset_url}',
                            'no-reply@mywebsite.com',
                            [email],
                        )
                    return JsonResponse({"message": "An email has been sent with instructions to reset your password."})
                else:
                    return JsonResponse({"error": "No user found with this email address."})

            return JsonResponse({"error": "Invalid email address."})
        
        form = PasswordResetForm()
        return render(request, 'password/password_reset.html', {'form': form})

    # Password Reset Confirm
    else:
        try:
            uid = urlsafe_base64_decode(uidb64)  # Corrected line: no .decode() needed
            user = get_user_model().objects.get(pk=uid)  # Get the user object
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({"error": "Invalid link."})

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    login(request, user)  # Log the user in automatically
                    return redirect('login')  # Redirect to the login page after resetting password

                else:
                    return JsonResponse({"error": "Passwords do not match."})

            form = SetPasswordForm(user)
            return render(request, 'password/password_reset.html', {'form': form, 'reset': True})

        return JsonResponse({"error": "The reset link is invalid or expired."})



from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

def main(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to the previous page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
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

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import LoginForm  # Ensure you import your LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')  # Redirect to a home page after login
        else:
            # Add an error message if the form is not valid
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'myApp/login.html', {'form': form})

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('') 



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
            portfolio.user = request.user  # Automatically set the logged-in user
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
            return redirect('template_list')  # Redirect to the desired page after saving
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
@login_required
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
            aboutme = form.save(commit=False)  # Create the object but don't save yet
            aboutme.user = request.user  # Assign the logged-in user to the object

            # Set the category to "Template1"
            template2_category = Category.objects.get(type='template2')
            aboutme.category = template2_category  # Assign the category

            aboutme.save()  # Save the object
            return redirect('template2_list')  # Redirect to the desired page after saving
    else:
        form = AboutMeForm()  # Create a new form instance for GET requests

    return render(request, 'myApp/temp2/template2.html', {'form': form})  # R
@login_required
def template2_list(request):
    # Filter profiles by the logged-in user and the specified category
    template2_category = Category.objects.get(type='template2')
    about_me_profiles = AboutMe.objects.filter(user=request.user, category=template2_category)
    print(about_me_profiles)  # Check the filtered profiles in your console

    return render(request, 'myApp/temp2/savedTemplate2.html', {
        'templates': about_me_profiles
    })

@login_required
def Template2EditView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES, instance=about_me)
        if form.is_valid():
            form.save()
            return redirect('template2_list')
    else:
        form = AboutMeForm(instance=about_me)

    return render(request, 'myApp/temp2/edit_template2.html', {'form': form})

@login_required
def Template2DeleteView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        about_me.delete()
        return redirect('main')

    return render(request, 'myApp/temp2/savedTemplate2.html', {'about_me': about_me})




@login_required
def Template3CreateView(request):
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES)  
        if form.is_valid():
            aboutme = form.save(commit=False)  
            aboutme.user = request.user 
            template3_category = Category.objects.get(type='template3')
            aboutme.category = template3_category  
            aboutme.save()  
            return redirect('template3_list')  
    else:
        form = AboutMeForm()  

    return render(request, 'myApp/temp3/template3.html', {'form': form})  
@login_required
def template3_list(request):
    template3_category = Category.objects.get(type='template3')
    about_me_profiles = AboutMe.objects.filter(user=request.user, category=template3_category)
    print(about_me_profiles) 
    
    return render(request, 'myApp/temp3/savedTemplate3.html', {
        'templates': about_me_profiles
    })


@login_required
def Template3EditView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES, instance=about_me)
        if form.is_valid():
            form.save()
            return redirect('template3_list')
    else:
        form = AboutMeForm(instance=about_me)

    return render(request, 'myApp/temp3/edit_template3.html', {'form': form})

@login_required
def Template3DeleteView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        about_me.delete()
        return redirect('main')

    return render(request, 'myApp/temp3/savedTemplate3.html', {'about_me': about_me})




@login_required
def Template4CreateView(request):
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES)  
        if form.is_valid():
            aboutme = form.save(commit=False)  
            aboutme.user = request.user 
            template3_category = Category.objects.get(type='template4')
            aboutme.category = template3_category  
            aboutme.save()  
            return redirect('template4_list')  
    else:
        form = AboutMeForm()  

    return render(request, 'myApp/temp4/template4.html', {'form': form})  
@login_required
def template4_list(request):
    template3_category = Category.objects.get(type='template4')
    about_me_profiles = AboutMe.objects.filter(user=request.user, category=template3_category)
    print(about_me_profiles) 
    
    return render(request, 'myApp/temp4/savedTemplate4.html', {
        'templates': about_me_profiles
    })



@login_required
def Template4EditView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES, instance=about_me)
        if form.is_valid():
            form.save()
            return redirect('template4_list')
    else:
        form = AboutMeForm(instance=about_me)

    return render(request, 'myApp/temp4/edit_template4.html', {'form': form})

@login_required
def Template4DeleteView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        about_me.delete()
        return redirect('main')

    return render(request, 'myApp/temp4/savedTemplate4.html', {'about_me': about_me})


@login_required
def Template5CreateView(request):
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES)  
        if form.is_valid():
            aboutme = form.save(commit=False)  
            aboutme.user = request.user 
            template3_category = Category.objects.get(type='template5')
            aboutme.category = template3_category  
            aboutme.save()  
            return redirect('template5_list')  
    else:
        form = AboutMeForm()  

    return render(request, 'myApp/temp5/template5.html', {'form': form})  
@login_required
def template5_list(request):
    template3_category = Category.objects.get(type='template5')
    about_me_profiles = AboutMe.objects.filter(user=request.user, category=template3_category)
    print(about_me_profiles) 
    
    return render(request, 'myApp/temp5/savedTemplate5.html', {
        'templates': about_me_profiles
    })



@login_required
def Template5EditView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AboutMeForm(request.POST, request.FILES, instance=about_me)
        if form.is_valid():
            form.save()
            return redirect('template5_list')
    else:
        form = AboutMeForm(instance=about_me)

    return render(request, 'myApp/temp5/edit_template5.html', {'form': form})

@login_required
def Template5DeleteView(request, pk):
    about_me = get_object_or_404(AboutMe, pk=pk, user=request.user)
    if request.method == 'POST':
        about_me.delete()
        return redirect('main')

    return render(request, 'myApp/temp5/savedTemplate5.html', {'about_me': about_me})

