import io
import json
from django.http import HttpResponse, JsonResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt


def students_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')
    # return JsonResponse(serializer.data, safe=False)

def student_detail(request, pk):
    try:
        student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student)
        # json_data = JSONRenderer().render(serializer.data)
        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(serializer.data)
    except Exception as e:
        return HttpResponse('Error: ' + str(e))


@csrf_exempt
def student_create(request):
    if request.method == 'POST':
        try:
            data = request.body
            stream = io.BytesIO(data)
            data = JSONParser().parse(stream)
            serializer = StudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': 'Student has been created'
                }
                # data = json.dumps(response)
                data = JSONRenderer().render(response)
                return HttpResponse(data, content_type='application/json')
            response = JSONRenderer().render(serializer.errors)
            return HttpResponse(response, content_type='application/json')
        except Exception as e:
            return HttpResponse('Exception: ' + str(e))
    else:
        return HttpResponse('Only Post request is allowed!')



