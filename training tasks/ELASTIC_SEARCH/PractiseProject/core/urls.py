# core/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('search/', include('search.urls')), # new
    path('admin/', admin.site.urls),
]