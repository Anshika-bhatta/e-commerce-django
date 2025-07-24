from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

@api_view(['GET'])
def product_search_api(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_history_api(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def featured_products_api(request):
    products = Product.objects.filter(is_featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)