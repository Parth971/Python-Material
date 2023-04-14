from django.db import models

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class Categorie(models.Model):
    category_name = models.CharField(max_length=100)

class Book(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=100)

class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to='excel')