from rest_framework import serializers
from ..models import HealthCard

class HealthCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCard
        fields = "__all__"
