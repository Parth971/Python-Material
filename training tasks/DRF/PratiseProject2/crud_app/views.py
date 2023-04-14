import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from serializer_app.serializers import StudentSerializer
from serializer_app.models import Student
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class StudentAPI(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)

        id = data.get('id', None)

        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'msg': 'Student Created'
            }
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data, content_type='application/json')

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'msg': 'Student Updated'
            }
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data, content_type='application/json')

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        response = {
            'msg': 'Student Deleted!'
        }
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data, content_type='application/json')
