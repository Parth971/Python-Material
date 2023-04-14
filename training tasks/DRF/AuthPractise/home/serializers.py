from dataclasses import field
from rest_framework import serializers
from home.models import Book, Categorie, Student
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['first_name', 'age', 'gender']
        # exclude = ['id']
        fields = '__all__'

    def validate(self, data):
        
        if data.get('age') and data['age'] < 18:
            raise serializers.ValidationError({'age': 'Student must be Adult.'})

        return data

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        # fields = '__all__'
        fields = ['category_name']

class BookSerializer(serializers.ModelSerializer):
    # categorie = CategorieSerializer() # takes ForeignKey
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1

