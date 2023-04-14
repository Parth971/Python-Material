from django.urls import path
from .views import student_create, students_list, student_detail


urlpatterns = [
    path('student/', students_list),
    path('student/<int:pk>/', student_detail),
    path('create-student/', student_create),
]
