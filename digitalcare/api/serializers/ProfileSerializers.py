from rest_framework import serializers
from ..models import (StudentProfile, VisitorProfile, AdultProfile)

class StudentProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('user',)


class VisitorProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)

    class Meta:
        model = VisitorProfile
        fields = '__all__'
        read_only_fields = ('user',)



class AdultProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)

    class Meta:
        model = AdultProfile
        fields = '__all__'
        read_only_fields = ('user',)
        

