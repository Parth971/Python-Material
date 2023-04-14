from django.contrib import admin
from home.models import Student, Categorie, Book

admin.site.register([Student, Categorie, Book])
