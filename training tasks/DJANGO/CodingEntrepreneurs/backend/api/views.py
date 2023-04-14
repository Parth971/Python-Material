from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
from products.models import Product

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    # get_data = request.GET
    # post_data = request.POST
    # body_data = request.body

    # data = {}

    # try:
    #     data = json.loads(body_data)
    # except:
    #     print('exception')

    # data['params'] = dict(get_data)
    # data['headers'] = dict(request.headers)
    # data['content_type'] = request.content_type

    # product = Product.objects.all().order_by("?").first()
    # data = {}
    # if product:
        # data = model_to_dict(product)
    #     data = ProductSerializer(product).data
    # return Response(data)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data)
        # instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid": "Not Good Data"}, status=400)
