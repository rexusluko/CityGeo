from rest_framework import serializers
from .models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'latitude', 'longitude']


class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']
