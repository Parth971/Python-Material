from rest_framework import generics, mixins
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixin
)
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions


class ProductDetailAPIView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListCreateAPIView(
        UserQuerySetMixin,
        StaffEditorPermissionMixin,
        generics.ListCreateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # allow_staff_view = False
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):   
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None

        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     user = self.request.user
        
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)


class ProductUpdateAPIView(
        StaffEditorPermissionMixin,
        generics.UpdateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()

        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(
        StaffEditorPermissionMixin,
        generics.DestroyAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class ProductMixinView(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request,*args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):   
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None

        if content is None:
            content = 'empty Content'
        serializer.save(content=content)