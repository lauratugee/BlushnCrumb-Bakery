from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from .models import Product, Order
from .forms import ProductForm, OrderForm, OrderItemFormSet
from django.contrib.auth.decorators import login_required
from django.db import transaction



def index(request):
    return render(request,"index.html")

def gallery(request):
    return render(request, "gallery.html")

def contact(request):
    return render(request, "contact.html")

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
            return render(request, "order_confirmation.html", {"order": order})

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

def user_login(request):
    if request.method == "POST":
        form=AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('index')

    else:
        form=AuthenticationForm()

    return render(request,"login.html",{"form":form})

def user_logout(request):
    logout(request)
    return redirect('index')



@login_required
def place_order(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        order = order_form.save(commit=False) if order_form.is_valid() else Order()
        order.customer = request.user
        formset = OrderItemFormSet(request.POST, instance=order)

        if order_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order.save()
                items = formset.save(commit=False)

                for item in items:
                    item.price = item.product.price
                    item.save()

                for item in formset.deleted_objects:
                    item.delete()

            return redirect('products')

    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, "place_order.html", {
        "order_form": order_form,
        "formset": formset,
    })

            



