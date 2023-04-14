from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'age']
        # read_only_fields = ['name']

# validator lvl
def camel_case(value):
    first_letter = value[0]
    rest_word = value[1:]
    if value[0] != first_letter.upper() or value[1:] != rest_word.lower():
        raise serializers.ValidationError('Name must be in camelCase!')


class StudentSimpleSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, validators=[camel_case])
    last_name = serializers.CharField(max_length=100, validators=[camel_case])
    age = serializers.IntegerField()

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance

    # field lvl
    def validate_age(self, value):
        if value >= 18:
            raise serializers.ValidationError('Student must be less than 18')
        return value

    # field object
    def validate(self, data):
        if data.get('first_name').lower() == 'parth' and data.get('age') != 20:
            raise serializers.ValidationError('Parth must be 20 years old!')
        return data
