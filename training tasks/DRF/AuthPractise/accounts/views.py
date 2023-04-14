from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from accounts.models import User
from rest_framework.response import Response
from accounts.helpers import send_otp_to_mobile


class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status_code': 200,
                    'message': 'Email and Otp is sent.',
                    'data': serializer.data
                })
            return Response({
                'status_code': 403,
                'errors': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status_code': 404,
                'errors': 'Something went wrong'
            })

class VerifyOtp(APIView):
    def post(self, request):
        try:
            data = request.data
            user_obj = User.objects.get(phone=data.get('phone'))
            otp = data.get('otp')
            
            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({
                    'status': 200,
                    'message': 'Your OTP has been Verified.'
                })
            return Response({
                    'status': 403,
                    'message': 'Your OTP is wrong.'
                })
        except Exception as e:
            print(e)

    def patch(self, request):
        try:
            data = request.data

            user_obj = User.objects.filter(phone=data.get('phone'))

            if not user_obj.exists():
                return Response({
                    'status': 404,
                    'message': 'No User found!'
                })
            status, time = send_otp_to_mobile(data.get('phone'), user_obj.first())
            if status:
                return Response({
                    'status': 200,
                    'message': 'New OTP Sent!'
                })

            return Response({
                    'status': 404,
                    'message': f'Try after few seconds({time})!'
                })
        except Exception as e:
            print(e)
            return Response({
                'status_code': 404,
                'errors': 'Something went wrong'
            })