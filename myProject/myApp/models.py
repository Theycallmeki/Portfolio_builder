from django.db import models
from django.contrib.auth.models import User  # Import the User model for linking portfolios to users
from ckeditor.fields import RichTextField

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios', null=True)
    title = models.CharField(max_length=200)
    description = RichTextField()

    def __str__(self):
        return self.title

class PortfolioElement(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='elements')  # Link to Portfolio
    content = RichTextField()
    media = models.ImageField(upload_to='media/', blank=True, null=True)  # Optional media upload
    order = models.IntegerField(default=0)  # Order of elements in the portfolio
    font = models.CharField(max_length=50, default='Arial')  # Font for the element
    color = models.CharField(max_length=7, default='#000000')  # Hex color code for the element

    def __str__(self):
        return f"Element {self.order} in {self.portfolio.title}"


from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Assuming you're using CKEditor for rich text

class Category(models.Model):
    # Define the type field to link it with AboutMe's type
    type = models.CharField(max_length=100, unique=True)  # Unique type for categories

    def __str__(self):
        return self.type

class AboutMe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='about_me', null=True)
    image = models.ImageField(upload_to='media/')
    description = models.CharField(max_length=200)
    background_nationality = models.CharField(max_length=100)
    background_hometown = models.CharField(max_length=100)
    background_languages = models.CharField(max_length=255)  # Comma-separated languages
    skills = models.CharField(max_length=255)  # Comma-separated skills
    education = models.CharField(max_length=255)  # Comma-separated education details
    experience = models.TextField()  # A detailed text field for experience
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='about_me_categories', null=True)

    def __str__(self):
        return f"{self.user.username}'s About Me"