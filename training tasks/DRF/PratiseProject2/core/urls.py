from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('serializer-app/', include('serializer_app.urls')),
    path('api/', include('api.urls')),
    path('crud/', include('crud_app.urls'))
]
