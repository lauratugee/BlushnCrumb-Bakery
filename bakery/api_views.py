from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .api_serializers import OrderCreateSerializer, OrderReadSerializer, ProductSerializer
from .models import Order, Product


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Product.objects.filter(stock__gt=0).order_by('name')


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order = Order.objects.prefetch_related('items__product').get(pk=order.pk)
        response_serializer = OrderReadSerializer(order, context=self.get_serializer_context())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class MyOrdersAPIView(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).prefetch_related('items__product').order_by('-order_date', '-id')
