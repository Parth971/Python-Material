from django.urls import path
# from home.views import get_students, post_students, put_students, patch_students, delete_students, StudentView
from home.views import GeneratePdf, ImportExportExcel, RegisterView, StudentView, get_book, StudentGenericForCreateAndList, StudentGenericForUpdateAndDelete

urlpatterns = [
    path('', StudentView.as_view(), name='students_view'),
    path('generic-student/', StudentGenericForCreateAndList.as_view(), name='students_create_list'),
    path('generic-student/<int:id>/', StudentGenericForUpdateAndDelete.as_view(), name='students_update_delete'),
    path('get-book/', get_book, name='get-book'),
    path('register/', RegisterView.as_view(), name='register'),
    path('pdf/', GeneratePdf.as_view(), name='generate-pdf'),
    path('excel/', ImportExportExcel.as_view(), name='import-export-excel'),
    # path('', get_students, name='get_students'),
    # path('post-student/', post_students, name='post_students'),
    # path('put-student/', put_students, name='put_students'),
    # path('patch-student/', patch_students, name='patch_students'),
    # path('delete-student/', delete_students, name='delete_students'),
]
