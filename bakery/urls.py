from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('products/',views.products,name='products'),
    path('add-product/',views.add_product,name='add_product'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('place-order/', views.place_order, name='place_order'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('staff/orders/', views.manage_orders, name='manage_orders'),
]
