from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def business_listings(request):
    return render(request, 'business/business_listings.html')

@login_required
def add_business(request):
    return render(request, "business/add_business.html")
