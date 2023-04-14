from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student2
from .serializer import Student2Serializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets


class StudentReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student2.objects.all()
    serializer_class = Student2Serializer


class StudentModelViewset(viewsets.ModelViewSet):
    queryset = Student2.objects.all()
    serializer_class = Student2Serializer


class StudentViewset(viewsets.ViewSet):
    def list(self, request):
        stu = Student2.objects.all()
        serializer = Student2Serializer(stu, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stud = Student2.objects.filter(id=id)
            if not stud.exists():
                msg = {
                    'message': 'No student with this id exists'
                }
                return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
            stud = stud.first()
            serializer = Student2Serializer(stud)
            return Response(serializer.data)
        msg = {
            'message': 'id not valid'
        }
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request):
        serializer = Student2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {'message': 'Student Added'}
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        id = pk
        if id is None:
            msg = {
                'message': 'id not given in url'
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        stud = Student2.objects.filter(id=id)

        if not stud.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stud = stud.first()
        serializer = Student2Serializer(stud, data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Updated Partially'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        id = pk
        if id is None:
            msg = {
                'message': 'id not given in url'
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        stud = Student2.objects.filter(id=id)

        if not stud.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stud = stud.first()
        serializer = Student2Serializer(stud, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Updated Partially'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        id = pk
        # For id check in PUT, PATCH, and DELETE method
        if id is None:
            msg = {
                'message': 'id not given in url'
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        stud = Student2.objects.filter(id=id)

        # For id exists check in PUT, PATCH, and DELETE method
        if not stud.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stud = stud.first()

        stud.delete()
        msg = {
            'message': 'Student Deleted'
        }
        return Response(msg, status=status.HTTP_200_OK)


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student2.objects.all()
    serializer_class = Student2Serializer


class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student2.objects.all()
    serializer_class = Student2Serializer
    lookup_field = 'id'


class StudentLCView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Student2.objects.all()
    serializer_class = Student2Serializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentRUDView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Student2.objects.all()
    serializer_class = Student2Serializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StudentAPI(APIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            stud = Student2.objects.filter(id=id)
            if not stud.exists():
                msg = {
                    'message': 'No student with this id exists'
                }
                return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
            stud = stud.first()
            serializer = Student2Serializer(stud)
            return Response(serializer.data, status=status.HTTP_200_OK)
        stud = Student2.objects.all()
        serializer = Student2Serializer(stud, many=True)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id=None, format=None):
        serializer = Student2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Added'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None, format=None):
        # For id check in PUT, PATCH, and DELETE method
        if id is None:
            msg = {
                'message': 'id not given in url'
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        stud = Student2.objects.filter(id=id)

        # For id exists check in PUT, PATCH, and DELETE method
        if not stud.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stud = stud.first()

        serializer = Student2Serializer(stud, data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Updated Fully'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None, format=None):
        # For id check in PUT, PATCH, and DELETE method
        if id is None:
            msg = {
                'message': 'id not given in url'
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        stud = Student2.objects.filter(id=id)

        # For id exists check in PUT, PATCH, and DELETE method
        if not stud.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stud = stud.first()

        serializer = Student2Serializer(stud, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Updated Partially'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, format=None):
        # For id check in PUT, PATCH, and DELETE method
        if id is None:
            msg = {
                'message': 'id not given in url'
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        stud = Student2.objects.filter(id=id)

        # For id exists check in PUT, PATCH, and DELETE method
        if not stud.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stud = stud.first()

        stud.delete()
        msg = {
            'message': 'Student Deleted'
        }
        return Response(msg, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def students(request, id=None):
    if request.method == 'GET':
        if id is not None:
            stud = Student2.objects.filter(id=id)
            if not stud.exists():
                msg = {
                    'message': 'No student with this id exists'
                }
                return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
            stud = stud.first()
            serializer = Student2Serializer(stud)
            return Response(serializer.data, status=status.HTTP_200_OK)
        stud = Student2.objects.all()
        serializer = Student2Serializer(stud, many=True)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = Student2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Added'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # For id check in PUT, PATCH, and DELETE method
    if id is None:
        msg = {
            'message': 'id not given in url'
        }
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    stud = Student2.objects.filter(id=id)

    # For id exists check in PUT, PATCH, and DELETE method
    if not stud.exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    stud = stud.first()

    if request.method == 'PUT':
        serializer = Student2Serializer(stud, data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Updated Fully'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        serializer = Student2Serializer(stud, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {
                'message': 'Student Updated Partially'
            }
            return Response(msg, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        stud.delete()
        msg = {
            'message': 'Student Deleted'
        }
        return Response(msg, status=status.HTTP_200_OK)