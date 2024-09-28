from django.contrib import admin
from .models import Portfolio, PortfolioElement,AboutMe,Category
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(PortfolioElement)
admin.site.register(AboutMe)
admin.site.register(Category)