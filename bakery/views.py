from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Product
from .forms import ProductForm

def index(request):
    return render(request,"index.html")

def proj_test(request):
    return render(request,"proj_test.html")

def products(request):
    all_products = Product.objects.all()

    return render(request, "products.html", {
        "products": all_products
    })
def add_product(request):
    if request.method == "POST":
        form=ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('products')

    else:
        form=ProductForm()

    return render(request,"add_product.html",{"form":form})

def register(request):
    if request.method == "POST":
        form=UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form=UserCreationForm()

    return render(request,"register.html",{"form":form})


