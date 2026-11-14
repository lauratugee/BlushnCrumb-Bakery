from django.shortcuts import render
from .models import Product

def index(request):
    return render(request,"index.html")

def proj_test(request):
    return render(request,"proj_test.html")

def products(request):
    all_products = Product.objects.all()

    return render(request, "products.html", {
        "products": all_products
    })


