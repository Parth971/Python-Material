from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
# router.register('student-api', views.StudentViewset, basename='student')
# router.register('student-api', views.StudentModelViewset, basename='student')
router.register('student-api', views.StudentReadOnlyModelViewSet, basename='student-read-only')

urlpatterns = [
    # path('students/', views.students),
    # path('students/<int:id>/', views.students),

    # path('students/', views.StudentAPI.as_view()),
    # path('students/<int:id>/', views.StudentAPI.as_view()),

    # path('students/', views.StudentLCView.as_view()),
    # path('students/<int:id>/', views.StudentRUDView.as_view()),

    # path('students/', views.StudentListCreateView.as_view()),
    # path('students/<int:id>/', views.StudentRetrieveUpdateDestroyView.as_view()),

    path('', include(router.urls))
]