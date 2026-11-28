from django.urls import include, path
from . import views
from . import api_views

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
    path('api/products/', api_views.ProductListAPIView.as_view(), name='api_products'),
    path('api/orders/', api_views.OrderCreateAPIView.as_view(), name='api_orders'),
    path('api/my-orders/', api_views.MyOrdersAPIView.as_view(), name='api_my_orders'),
    path('api-auth/', include('rest_framework.urls')),
]
