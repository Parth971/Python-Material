import datetime
import uuid
from django.conf import settings
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from home.helpers import save_pdf
from home.models import Book, ExcelFileUpload, Student
from home.serializers import BookSerializer, StudentSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

class StudentView(APIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        student_serializer = StudentSerializer(students, many=True)
        return Response({
            'status_code': 200,
            'message': 'All Students Fetched',
            'data': student_serializer.data
        })

    def post(self, request):
        data = request.data
        student_serializer = StudentSerializer(data=data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response({
                'status_code': 200,
                'message': 'Student is Saved',
                'data': student_serializer.data
            })
        return Response({
            'status_code': 403,
            'message': 'Student is not Saved',
            'errors': student_serializer.errors
        })

    def put(self, request):
        try:
            id = request.data.get('id')
            student = Student.objects.get(id=id)

            data = request.data
            student_serializer = StudentSerializer(student, data=data, partial=False)
            if student_serializer.is_valid():
                student_serializer.save()
                return Response({
                    'status_code': 200,
                    'message': 'Student is Updated',
                    'data': student_serializer.data
                })
        
            return Response({
                'status_code': 403,
                'message': 'Student is not Updated',
                'errors': student_serializer.errors
            })
        except Exception as e:
            return Response({
                'status_code': 403,
                'message': 'Student is not Updated',
                'exception': str(e)
            })

    def patch(self, request):
        try:
            id = request.data.get('id')
            student = Student.objects.get(id=id)

            data = request.data
            student_serializer = StudentSerializer(student, data=data, partial=True)
            if student_serializer.is_valid():
                student_serializer.save()
                return Response({
                    'status_code': 200,
                    'message': 'Student is Updated',
                    'data': student_serializer.data
                })
        
            return Response({
                'status_code': 403,
                'message': 'Student is not Updated',
                'errors': student_serializer.errors
            })
        except Exception as e:
            return Response({
                'status_code': 403,
                'message': 'Student is not Updated',
                'exception': str(e)
            })

    def delete(self, request):
        try:
            id = request.data.get('id')
            student = Student.objects.get(id=id)
            student.delete()
            return Response({
                'status_code': 200,
                'message': 'Student is Deleted'
            })
        except Exception as e:
            return Response({
                'status_code': 403,
                'message': 'Student is not Deleted',
                'exception': str(e)
            })
  
@api_view()
def get_book(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({
        'status_code': 200,
        'message': 'All Books.',
        'data': serializer.data
    }) 

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=serializer.data['username'])
            # token_obj, _ = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)

            return Response({
                'status_code': 200,
                'message': 'User is Saved',
                'data': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({
            'status_code': 403,
            'message': 'User is not Saved',
            'errors': serializer.errors
        })

class StudentGenericForCreateAndList(generics.CreateAPIView, generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentGenericForUpdateAndDelete(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'

class GeneratePdf(APIView):
    def get(self, request):
        student_objs = Student.objects.all()
        params = {
            'today': datetime.date.today(),
            'student_objs': student_objs
        }
        file_name, status = save_pdf(params)
        if status:
            return Response({'status': 200, 'filename': f'/media/{file_name}.pdf'})
        return Response({'status': 400})

class ImportExportExcel(APIView):
    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)

        df = pd.DataFrame(serializer.data)
        print(df)
        df.to_csv(f'public/static/excel/{uuid.uuid4()}.csv', encoding='UTF-8', index=False)
        return Response({'status': 200})

    def post(self, request):
        exceled_object = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files'])
        df = pd.read_csv(f'{settings.BASE_DIR}/public/static/{exceled_object.excel_file_upload}')
        print(df.values.tolist())

        return Response({'status': 200})






# @api_view(['GET'])
# def get_students(request):
#     students = Student.objects.all()
#     student_serializer = StudentSerializer(students, many=True)
#     return Response({
#         'status_code': 200,
#         'message': 'All Students Fetched',
#         'data': student_serializer.data
#     })

# @api_view(['POST'])
# def post_students(request):
#     data = request.data
#     student_serializer = StudentSerializer(data=data)
#     if student_serializer.is_valid():
#         student_serializer.save()
#         return Response({
#             'status_code': 200,
#             'message': 'Student is Saved',
#             'data': student_serializer.data
#         })
#     return Response({
#         'status_code': 403,
#         'message': 'Student is not Saved',
#         'errors': student_serializer.errors
#     })

# @api_view(['PUT'])
# def put_students(request):
#     try:
#         id = request.data.get('id')
#         student = Student.objects.get(id=id)

#         data = request.data
#         student_serializer = StudentSerializer(student, data=data, partial=False)
#         if student_serializer.is_valid():
#             student_serializer.save()
#             return Response({
#                 'status_code': 200,
#                 'message': 'Student is Updated',
#                 'data': student_serializer.data
#             })
    
#         return Response({
#             'status_code': 403,
#             'message': 'Student is not Updated',
#             'errors': student_serializer.errors
#         })
#     except Exception as e:
#         return Response({
#             'status_code': 403,
#             'message': 'Student is not Deleted',
#             'exception': str(e)
#         })

# @api_view(['PATCH'])
# def patch_students(request):
#     try:
#         id = request.data.get('id')
#         student = Student.objects.get(id=id)

#         data = request.data
#         student_serializer = StudentSerializer(student, data=data, partial=True)
#         if student_serializer.is_valid():
#             student_serializer.save()
#             return Response({
#                 'status_code': 200,
#                 'message': 'Student is Updated',
#                 'data': student_serializer.data
#             })
    
#         return Response({
#             'status_code': 403,
#             'message': 'Student is not Updated',
#             'errors': student_serializer.errors
#         })
#     except Exception as e:
#         return Response({
#             'status_code': 403,
#             'message': 'Student is not Deleted',
#             'exception': str(e)
#         })

# @api_view(['DELETE'])
# def delete_students(request):
#     try:
#         id = request.data.get('id')
#         student = Student.objects.get(id=id)
#         student.delete()
#         return Response({
#             'status_code': 200,
#             'message': 'Student is Deleted'
#         })
#     except Exception as e:
#         return Response({
#             'status_code': 403,
#             'message': 'Student is not Deleted',
#             'exception': str(e)
#         })