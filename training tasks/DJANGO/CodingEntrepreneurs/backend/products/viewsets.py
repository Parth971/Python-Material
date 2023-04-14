from rest_framework import viewsets, mixins
from .models import Product
from .serializers import ProductSerializer

class ProductViewset(viewsets.ModelViewSet):
    '''
        This accepts all methods GET, POST, etc
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

class ProductGenericViewset(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
    ):
    '''
        This accepts one methods GET for listing, and retriving
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'