from django.shortcuts import render

def index(request):
    return render(request,"index.html")

def proj_test(request):
    return render(request,"proj_test.html")


