from rest_framework import serializers
from .models import Student2


class Student2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student2
        fields = ['id', 'name', 'roll', 'city']
        read_only_fields = ['id']