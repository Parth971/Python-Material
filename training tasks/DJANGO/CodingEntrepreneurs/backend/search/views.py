from rest_framework.response import Response
from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer
from . import client


class SearchListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:
            user = request.user.username

        query = request.GET.get('q')
        
        public = str(request.GET.get('public')) != '0'
        
        tag = request.GET.get('tag') or None
        if query is None:
            return Response('', status=400)

        print(query, tag, user, public)

        results = client.perform_search(query=query, tags=tag, user=user, public=public)
        return Response(results)


class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        result = Product.objects.none()
        q = self.request.GET.get('q')
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            result = qs.search(query=q, user=user)
        return result