from requests import request
from rest_framework import serializers
from .models import Product
from rest_framework.reverse import reverse
from .validators import validate_title_no_hello, unique_product_title
from api.serializers import UserPubliSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPubliSerializer(source='user', read_only=True)
    # related_products = ProductInlineSerializer(source='user.product_set.all', many=True, read_only=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk'
    )
    # email = serializers.EmailField(source='user.email', read_only=True)
    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title])
    class Meta:
        model = Product
        fields = [
            'owner',
            # 'email',
            'url',
            'edit_url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'public'
            # 'my_discount',
            # 'my_user_data',
            # 'related_products'
        ]

    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username
        }


    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-update', kwargs={'pk': obj.pk}, request=request)

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()