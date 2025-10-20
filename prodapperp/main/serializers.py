
from rest_framework import serializers
from .models import DziennikZdarzenRCP

class DziennikZdarzenRCPSerializer(serializers.ModelSerializer):
    class Meta:
        model = DziennikZdarzenRCP
        fields = '__all__'
